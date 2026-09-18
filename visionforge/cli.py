import argparse
import sys
import os
import cv2
import numpy as np

from visionforge.common.io_utils import load_image, save_image, save_point_cloud_ply
from visionforge.common.metrics import calculate_psnr, calculate_entropy
from visionforge.lowlevel.filters import apply_box_blur, apply_gaussian_blur, apply_laplacian
from visionforge.lowlevel.frequency import compute_fft_spectrum, apply_frequency_filter
from visionforge.lowlevel.transforms import rotate_image, apply_perspective_transform
from visionforge.lowlevel.histogram import equalize_histogram, apply_clahe
from visionforge.features.edges_corners import detect_canny_edges, detect_harris_corners, detect_hough_lines
from visionforge.features.descriptors import extract_and_match_features
from visionforge.features.segmentation import segment_otsu, segment_kmeans
from visionforge.stereo_3d.depth_reconstruction import compute_disparity_map, disparity_to_point_cloud
from visionforge.stereo_3d.rectification import stitch_images_homography
from visionforge.motion_pattern.background_sub import compute_frame_difference
from visionforge.motion_pattern.optical_flow import compute_dense_optical_flow, compute_sparse_optical_flow
from visionforge.motion_pattern.dimensionality import compress_image_pca
from visionforge.shape_from_x.photometric_stereo import compute_photometric_stereo, integrate_normals_to_depth


def handle_lowlevel(args):
    img = load_image(args.input)
    print(f"Loaded image: {args.input}, shape: {img.shape}")
    
    if args.action == "blur":
        out = apply_box_blur(img)
    elif args.action == "gaussian":
        out = apply_gaussian_blur(img)
    elif args.action == "laplacian":
        out = apply_laplacian(img)
    elif args.action == "fft":
        out = compute_fft_spectrum(img)
    elif args.action == "fft_lowpass":
        out = apply_frequency_filter(img, "lowpass", radius=30)
    elif args.action == "rotate":
        out = rotate_image(img, 45)
    elif args.action == "hist":
        out = equalize_histogram(img)
    elif args.action == "clahe":
        out = apply_clahe(img)
    else:
        print(f"Unknown action: {args.action}")
        return
        
    save_image(args.output, out)
    print(f"Saved result to: {args.output}")
    if len(img.shape) == len(out.shape) and img.shape == out.shape:
        psnr = calculate_psnr(img, out)
        print(f"PSNR with original: {psnr:.2f} dB")
    print(f"Output entropy: {calculate_entropy(out):.2f}")


def handle_features(args):
    img = load_image(args.input)
    print(f"Loaded image: {args.input}")
    
    if args.action == "canny":
        out = detect_canny_edges(img)
    elif args.action == "harris":
        out = detect_harris_corners(img)
    elif args.action == "hough":
        out = detect_hough_lines(img)
    elif args.action == "otsu":
        out = segment_otsu(img)
    elif args.action == "kmeans":
        out = segment_kmeans(img, k=3)
    elif args.action == "match":
        if not args.input2:
            print("Error: --input2 is required for feature matching.")
            return
        img2 = load_image(args.input2)
        out, count = extract_and_match_features(img, img2, method="orb")
        print(f"Found {count} matched features.")
    else:
        print(f"Unknown action: {args.action}")
        return
        
    save_image(args.output, out)
    print(f"Saved result to: {args.output}")


def handle_stereo(args):
    left = load_image(args.left)
    right = load_image(args.right)
    print(f"Loaded left and right stereo images.")
    
    disp = compute_disparity_map(left, right)
    disp_vis = cv2.normalize(disp, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    save_image(args.output, disp_vis)
    print(f"Saved disparity visualization to: {args.output}")
    
    if args.ply:
        pts, colors = disparity_to_point_cloud(disp, left)
        save_point_cloud_ply(args.ply, pts, colors)
        print(f"Exported {len(pts)} 3D points to: {args.ply}")


def handle_motion(args):
    f1 = load_image(args.frame1)
    f2 = load_image(args.frame2)
    print(f"Loaded frames for motion analysis.")
    
    if args.action == "diff":
        out = compute_frame_difference(f1, f2)
    elif args.action == "dense_flow":
        out, _ = compute_dense_optical_flow(f1, f2)
    elif args.action == "sparse_flow":
        out, count = compute_sparse_optical_flow(f1, f2)
        print(f"Tracked {count} motion vectors.")
    elif args.action == "pca":
        gray = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY) if len(f1.shape) == 3 else f1
        out, var_ratio = compress_image_pca(gray, n_components=20)
        print(f"PCA explained variance ratio: {var_ratio * 100:.2f}%")
    else:
        print(f"Unknown action: {args.action}")
        return
        
    save_image(args.output, out)
    print(f"Saved result to: {args.output}")


def handle_shape(args):
    imgs = [load_image(p) for p in args.inputs]
    print(f"Loaded {len(imgs)} illumination images for Photometric Stereo.")
    
    # 4 standard light directions [x, y, z]
    lights = [
        [0.0, 0.577, 0.816],
        [0.577, 0.0, 0.816],
        [0.0, -0.577, 0.816],
        [-0.577, 0.0, 0.816]
    ]
    if len(imgs) != len(lights):
        lights = [[0, 0, 1] for _ in range(len(imgs))]
        
    normal_map, albedo_map, vis_normal = compute_photometric_stereo(imgs, lights)
    _, vis_depth = integrate_normals_to_depth(normal_map)
    
    normal_path = args.output
    base, ext = os.path.splitext(normal_path)
    depth_path = f"{base}_depth{ext}"
    albedo_path = f"{base}_albedo{ext}"
    
    save_image(normal_path, vis_normal)
    save_image(depth_path, vis_depth)
    save_image(albedo_path, albedo_map)
    print(f"Saved normal map to: {normal_path}")
    print(f"Saved depth map to: {depth_path}")
    print(f"Saved albedo map to: {albedo_path}")


def main():
    parser = argparse.ArgumentParser(description="VisionForge: Computer Vision CLI Toolkit")
    subparsers = parser.add_subparsers(dest="command", help="Module to run")
    
    # Low-level command
    p_low = subparsers.add_parser("lowlevel", help="Low-level processing and filtering")
    p_low.add_argument("--input", "-i", required=True, help="Input image path")
    p_low.add_argument("--output", "-o", required=True, help="Output image path")
    p_low.add_argument("--action", "-a", required=True, 
                       choices=["blur", "gaussian", "laplacian", "fft", "fft_lowpass", "rotate", "hist", "clahe"])
                       
    # Features command
    p_feat = subparsers.add_parser("features", help="Feature extraction and segmentation")
    p_feat.add_argument("--input", "-i", required=True, help="Input image path")
    p_feat.add_argument("--input2", help="Second image path for feature matching")
    p_feat.add_argument("--output", "-o", required=True, help="Output image path")
    p_feat.add_argument("--action", "-a", required=True, 
                        choices=["canny", "harris", "hough", "otsu", "kmeans", "match"])
                        
    # Stereo command
    p_stereo = subparsers.add_parser("stereo", help="Stereo vision and 3D reconstruction")
    p_stereo.add_argument("--left", "-l", required=True, help="Left stereo image path")
    p_stereo.add_argument("--right", "-r", required=True, help="Right stereo image path")
    p_stereo.add_argument("--output", "-o", required=True, help="Disparity map output path")
    p_stereo.add_argument("--ply", help="Optional output path for .ply point cloud")
    
    # Motion command
    p_motion = subparsers.add_parser("motion", help="Motion and pattern analysis")
    p_motion.add_argument("--frame1", "-f1", required=True, help="First frame image path")
    p_motion.add_argument("--frame2", "-f2", required=True, help="Second frame image path")
    p_motion.add_argument("--output", "-o", required=True, help="Output image path")
    p_motion.add_argument("--action", "-a", required=True, 
                          choices=["diff", "dense_flow", "sparse_flow", "pca"])
                          
    # Shape command
    p_shape = subparsers.add_parser("shape", help="Photometric Stereo shape recovery")
    p_shape.add_argument("--inputs", "-i", nargs="+", required=True, help="Input images under different lights")
    p_shape.add_argument("--output", "-o", required=True, help="Output normal map path")
    
    args = parser.parse_args()
    if args.command == "lowlevel":
        handle_lowlevel(args)
    elif args.command == "features":
        handle_features(args)
    elif args.command == "stereo":
        handle_stereo(args)
    elif args.command == "motion":
        handle_motion(args)
    elif args.command == "shape":
        handle_shape(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
