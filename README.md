# VisionForge: Computer Vision Coursework Project

**VIT Bhopal University**  
**Course**: Computer Vision  
**Faculty**: Dr. Gaurav Soni  
**Student Name**: Paarth Juneja  
**Registration Number**: 24BAI10160  

---

## Project Overview

VisionForge is a command-line project created for the Computer Vision course (VITyarthi project submission). It puts together algorithms from all 5 units of our course syllabus into one Python project:

1. **Unit 1: Low-Level Image Processing** - Image filtering (Box blur, Gaussian blur, Laplacian), 2D Fourier Transform (FFT magnitude and lowpass filter), geometric transformations (rotation, translation, affine, projective), and histogram equalization / CLAHE.
2. **Unit 2: Stereo Vision & 3D Reconstruction** - Stereo disparity calculation using StereoSGBM, epipolar lines with Fundamental matrix, homography stitching, and 3D point cloud export (`.ply` format).
3. **Unit 3: Feature Detection & Segmentation** - Canny edge detection, Harris corner detection, Hough line transform, SIFT and ORB feature matching, image pyramids, Otsu thresholding, and K-Means color segmentation.
4. **Unit 4: Motion & Pattern Analysis** - Frame differencing, MOG2 background subtraction, Farneback dense optical flow, Lucas-Kanade sparse feature tracking, and PCA image compression.
5. **Unit 5: Shape from X** - Photometric Stereo for calculating surface normals, albedo, and 3D depth maps from multiple images taken under different light directions.

---

## Features

- Complete coverage of syllabus units 1 to 5.
- Unified command-line interface with subcommands for each module (`lowlevel`, `features`, `stereo`, `motion`, `shape`).
- Sample data generator that creates test images locally.
- 3D point cloud export to `.ply` file format, which can be viewed in MeshLab or Blender.
- Image quality metrics: PSNR, MSE, and Shannon Entropy.
- Automated unit test suite using `pytest`.

---

## Project Structure

```
cv/
├── visionforge/
│   ├── common/             # Image I/O, PLY writer, and metric calculations
│   ├── lowlevel/           # Spatial filters, FFT, transforms, histogram
│   ├── features/           # Canny, Harris, matching, pyramids, segmentation
│   ├── stereo_3d/          # Epipolar geometry, SGBM disparity, 3D point cloud
│   ├── motion_pattern/     # Frame diff, optical flow, PCA
│   ├── shape_from_x/       # Photometric stereo, normal & depth recovery
│   └── cli.py              # Main CLI entry point
├── data/                   # Sample images and generator script
├── tests/                  # Unit tests for all modules
├── docs/
│   ├── diagrams/           # Architecture, workflow, and UML diagrams
│   └── figures/            # Output visual result figures
├── requirements.txt        # Required Python packages
├── run_all.py              # Script to run all tests and demos in one command
├── README.md
└── statement.md
```

---

## Installation & Setup

1. **Clone or open the repository folder**:
   ```bash
   cd cv
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate the sample images**:
   ```bash
   python data/generate_samples.py
   ```

---

## Quick Demo

To run all unit tests and sample commands at once:
```bash
python run_all.py
```
This will run the sample generator, execute all 12 unit tests, and save sample outputs to the `output/` directory.

---

## Usage Examples

You can also run each module individually from the command line:

### 1. Low-Level Processing
```bash
# Gaussian blur
python -m visionforge.cli lowlevel -i data/input_sample.png -o output/blur.png -a gaussian

# 2D FFT magnitude spectrum
python -m visionforge.cli lowlevel -i data/input_sample.png -o output/fft.png -a fft

# Histogram equalization (CLAHE)
python -m visionforge.cli lowlevel -i data/input_sample.png -o output/clahe.png -a clahe
```

### 2. Feature Detection & Segmentation
```bash
# Canny edge detector
python -m visionforge.cli features -i data/input_sample.png -o output/canny.png -a canny

# Harris corner detector
python -m visionforge.cli features -i data/input_sample.png -o output/harris.png -a harris

# Otsu thresholding
python -m visionforge.cli features -i data/input_sample.png -o output/otsu.png -a otsu

# K-Means segmentation
python -m visionforge.cli features -i data/input_sample.png -o output/kmeans.png -a kmeans
```

### 3. Stereo Vision & 3D Reconstruction
```bash
# Calculate disparity map and export 3D point cloud
python -m visionforge.cli stereo -l data/stereo_left.png -r data/stereo_right.png -o output/disparity.png --ply output/points.ply
```

### 4. Motion Analysis & PCA
```bash
# Dense optical flow
python -m visionforge.cli motion -f1 data/motion_frame1.png -f2 data/motion_frame2.png -o output/flow.png -a dense_flow

# PCA image compression
python -m visionforge.cli motion -f1 data/input_sample.png -f2 data/input_sample.png -o output/pca.png -a pca
```

### 5. Shape from X (Photometric Stereo)
```bash
# Recover surface normals, albedo, and depth
python -m visionforge.cli shape -i data/light1.png data/light2.png data/light3.png data/light4.png -o output/normals.png
```

---

## Running Unit Tests

Run the test suite with pytest:
```bash
python -m pytest -v
```
All 12 unit tests should pass.

---

## Results and Diagrams

All design diagrams and sample output results are stored in the `docs/` directory:
- `docs/diagrams/architecture_diagram.png`: System architecture
- `docs/diagrams/workflow_diagram.png`: Processing workflow
- `docs/diagrams/usecase_diagram.png`: Use case diagram
- `docs/diagrams/class_diagram.png`: Component & package structure
- `docs/diagrams/sequence_diagram.png`: Sequence diagram for stereo reconstruction
- `docs/figures/`: Sample visual output comparisons across all 5 modules
