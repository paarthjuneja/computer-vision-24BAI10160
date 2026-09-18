# Project Statement: VisionForge

**VIT Bhopal University**  
**Course**: Computer Vision  
**Faculty**: Dr. Gaurav Soni  
**Student Name**: Paarth Juneja  
**Registration Number**: 24BAI10160  

---

## 1. Problem Statement
In our computer vision course, we study many different topics such as low-level filtering, stereo depth estimation, feature extraction, motion tracking, and 3D shape recovery. Usually, these algorithms are written as separate, individual scripts, which makes it difficult to see how all the concepts fit together in a practical workflow.

VisionForge addresses this by bringing together the key methods taught across the five syllabus units into a single, modular Python project with a straightforward command-line interface.

## 2. Scope of the Project
The scope of VisionForge covers the syllabus topics across 5 units:
- **Unit 1**: Low-level image processing (spatial convolution, 2D FFT frequency filtering, geometric transformations, and histogram equalization / CLAHE).
- **Unit 2**: Stereo depth estimation, epipolar geometry, image stitching, and 3D point cloud generation (.ply format).
- **Unit 3**: Feature detection (Canny, Harris, Hough), feature matching (SIFT, ORB), image pyramids, and image segmentation (Otsu, K-Means).
- **Unit 4**: Motion analysis (frame differencing, background subtraction, optical flow) and pattern analysis (PCA compression).
- **Unit 5**: Shape from X (Photometric Stereo surface normal, albedo, and depth estimation).

## 3. Target Users
- Students studying computer vision who want clear and working reference implementations.
- Anyone looking for a simple tool to test and visualize classical computer vision algorithms from the terminal.

## 4. High-Level Features
- **Low-Level Module**: Filters images using Box, Gaussian, and Laplacian kernels; computes 2D FFT spectrum and lowpass filters; performs image rotation, affine, and perspective warps; and enhances contrast with CLAHE.
- **Stereo 3D Module**: Calculates disparity maps from stereo image pairs using StereoSGBM and saves 3D coordinates as a .ply point cloud file.
- **Features Module**: Detects edges and corners, matches keypoints across two images, builds multi-scale image pyramids, and segments images using Otsu and K-Means.
- **Motion & Pattern Module**: Detects movement using frame differencing and MOG2, computes dense and sparse optical flow vectors, and applies PCA for image compression.
- **Shape From X Module**: Calculates surface normals, albedos, and reconstructed 3D depth maps from images taken under multiple calibrated light sources.
- **CLI Interface**: A simple command-line interface with subcommands for each module and easy-to-use flags.
