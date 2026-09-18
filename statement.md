# Project Statement: VisionForge

## 1. Problem Statement
Computer vision involves many core techniques such as image filtering, feature extraction, 3D stereo reconstruction, motion analysis, and shape recovery. In many learning environments, students and researchers write disconnected scripts for each concept. This makes it difficult to understand how these algorithms connect together in a real workflow. 

VisionForge solves this problem by providing a simple, beginner-friendly command-line toolkit that brings together essential computer vision techniques from the course syllabus into one modular project.

## 2. Scope of the Project
The scope of VisionForge includes five key areas of computer vision:
- Low-level image processing (spatial filters, 2D FFT, transformations, histogram equalization)
- Multi-camera stereo vision (disparity mapping, epipolar lines, 3D point cloud export)
- Feature extraction and segmentation (Canny edges, Harris corners, ORB/SIFT matching, K-means/Otsu segmentation)
- Pattern and motion analysis (background subtraction, optical flow, PCA dimension reduction)
- Shape from X (Photometric Stereo surface normal and albedo estimation)

The project is implemented in Python using OpenCV, NumPy, and standard libraries, accessible via a straightforward CLI.

## 3. Target Users
- Computer Vision students and beginners who want hands-on code examples.
- Instructors and teaching assistants looking for a clean demonstration tool.
- Developers needing simple, standalone reference implementations for fundamental CV tasks.

## 4. High-Level Features
- **Low-Level Module**: Apply Gaussian, Bilateral, Laplacian filters, frequency domain FFT filtering, image rotation/translation/affine warping, and contrast enhancement.
- **Stereo & 3D Module**: Compute disparity maps from stereo pairs, draw epipolar lines, and save 3D coordinates as a .ply point cloud file.
- **Features & Segmentation Module**: Detect edges and corners, match keypoints between two images using ORB/SIFT, and segment images using Otsu and K-means clustering.
- **Motion & Pattern Module**: Detect moving objects using background subtraction, compute optical flow vectors, and compress image vectors using PCA.
- **Shape From X Module**: Estimate surface normal vectors and albedos from multiple images taken under different light directions (Photometric Stereo).
- **CLI Interface**: A simple command-line interface with clear commands for each module.
