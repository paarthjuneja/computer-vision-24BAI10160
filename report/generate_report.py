import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class StudentReport(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

    def chapter_title(self, num_str, title):
        self.set_font("Times", "B", 14)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, f"{num_str}. {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def section_title(self, title):
        self.set_font("Times", "B", 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 7, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def body_text(self, text):
        self.set_font("Times", "", 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet_point(self, title, text):
        self.set_font("Times", "B", 11)
        self.set_text_color(0, 0, 0)
        self.cell(6, 5.5, "-", new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(38, 5.5, f"{title}: ", new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.set_font("Times", "", 11)
        self.multi_cell(0, 5.5, text)
        self.ln(1.5)

    def add_figure(self, img_path, w=155, caption=""):
        if os.path.exists(img_path):
            self.image(img_path, x=(210 - w) / 2, w=w)
            self.ln(2)
            if caption:
                self.set_font("Times", "I", 10)
                self.set_text_color(60, 60, 60)
                self.cell(0, 5, caption, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                self.ln(3)

def build_pdf(output_path="report/VisionForge_Project_Report.pdf"):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    pdf = StudentReport(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(18, 18, 18)

    # ----------------------------------------------------
    # COVER PAGE
    # ----------------------------------------------------
    pdf.add_page()
    pdf.ln(25)

    pdf.set_font("Times", "B", 18)
    pdf.cell(0, 9, "VIT Bhopal University", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 8, "Computer Vision VITyarthi Project Submission", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.ln(25)
    pdf.set_font("Times", "B", 16)
    pdf.cell(0, 8, "VisionForge: Modular Computer Vision Toolkit", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Times", "", 12)
    pdf.cell(0, 7, "Project Report and Implementation Documentation", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(40)
    pdf.set_font("Times", "B", 12)
    pdf.cell(0, 7, "Submitted by:", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    # Clean student details block
    details = [
        ("Name", "Paarth Juneja"),
        ("Reg. No", "24BAI10160"),
        ("Course", "Computer Vision"),
        ("Faculty", "Dr. Gaurav Soni")
    ]
    
    start_x = 60
    for label, val in details:
        pdf.set_x(start_x)
        pdf.set_font("Times", "B", 11)
        pdf.cell(35, 6, f"{label}:", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Times", "", 11)
        pdf.cell(60, 6, val, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(50)
    pdf.set_font("Times", "", 11)
    pdf.cell(0, 6, "School of Computing Science and Engineering", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 6, "2026", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ----------------------------------------------------
    # 2. INTRODUCTION & 3. PROBLEM STATEMENT
    # ----------------------------------------------------
    pdf.add_page()
    pdf.chapter_title("1", "Introduction")
    pdf.body_text(
        "Computer Vision is an important area of study that focuses on how computers can be made to gain "
        "high-level understanding from digital images or videos. In our course, we learned about fundamental "
        "concepts starting from digital image formation and basic spatial and frequency filters, to multi-camera "
        "depth estimation, feature extraction, motion analysis, and shape recovery from surface reflectance."
    )
    pdf.body_text(
        "For this project, I developed VisionForge, which is a modular command-line interface (CLI) toolkit written "
        "in Python. Instead of having separate scripts for each syllabus topic, VisionForge combines all the "
        "core techniques into a clean and organized structure that is easy to run, test, and understand."
    )

    pdf.ln(2)
    pdf.chapter_title("2", "Problem Statement")
    pdf.body_text(
        "When studying computer vision, many students write one-off code snippets for each lab exercise. This makes "
        "it hard to see how different computer vision tasks connect with each other. For example, how low-level filtering "
        "helps in edge detection, how epipolar geometry helps in stereo depth matching, or how multiple illumination "
        "images can be used to recover 3D shapes."
    )
    pdf.body_text(
        "The goal of this project is to build an integrated, beginner-friendly CLI project that covers the topics "
        "from all five units of the syllabus. It provides simple commands for image filtering, stereo reconstruction, "
        "feature detection, optical flow, and photometric stereo, with test cases and sample data included."
    )

    # ----------------------------------------------------
    # 3. REQUIREMENTS
    # ----------------------------------------------------
    pdf.ln(2)
    pdf.chapter_title("3", "Functional Requirements")
    pdf.body_text("The project includes five major functional modules corresponding to the syllabus units:")
    pdf.bullet_point("Module 1 (Low-Level)", "Spatial convolution (Gaussian blur, Box blur, Laplacian), 2D Fourier Transform (FFT magnitude spectrum and lowpass filtering), geometric transforms (rotation, translation, affine, projective), and contrast enhancement (Histogram Equalization and CLAHE).")
    pdf.bullet_point("Module 2 (Stereo 3D)", "Stereo depth estimation using Semi-Global Block Matching (SGBM), fundamental matrix computation, epipolar line drawing, homography-based image stitching, and 3D point cloud generation exported to .ply format.")
    pdf.bullet_point("Module 3 (Features)", "Edge detection using Canny, corner detection using Harris Corner Detector, Hough line transform, feature matching using SIFT and ORB, Gaussian/Laplacian pyramids, and segmentation using Otsu thresholding and K-Means clustering.")
    pdf.bullet_point("Module 4 (Motion)", "Motion detection using frame differencing, background subtraction with MOG2, dense optical flow using Farneback algorithm, sparse optical flow using Lucas-Kanade tracker, and image compression using Principal Component Analysis (PCA).")
    pdf.bullet_point("Module 5 (Shape from X)", "Photometric Stereo for recovering surface normal vectors and albedo maps from multiple directional light sources, and integrating surface gradients into a 3D depth map.")

    pdf.ln(2)
    pdf.chapter_title("4", "Non-Functional Requirements")
    pdf.bullet_point("Performance", "Fast execution using NumPy vectorization and optimized OpenCV routines so that processing takes less than a second per image.")
    pdf.bullet_point("Usability", "Clear and simple command-line arguments using argparse with helpful error messages and command guides.")
    pdf.bullet_point("Reliability", "Proper input validation so missing images or invalid parameters do not crash the program unexpectedly.")
    pdf.bullet_point("Maintainability", "Clean, modular code structure divided into separate packages and files, written in a simple and beginner-friendly style.")

    # ----------------------------------------------------
    # 5. SYSTEM ARCHITECTURE & 6. DESIGN DIAGRAMS
    # ----------------------------------------------------
    pdf.add_page()
    pdf.chapter_title("5", "System Architecture")
    pdf.body_text(
        "VisionForge is organized into three main layers: a CLI interface layer that receives arguments from the terminal, "
        "a core algorithm layer containing the 5 syllabus modules, and a common utility layer that handles loading, saving, "
        "and metric calculations."
    )
    pdf.add_figure("docs/diagrams/architecture_diagram.png", w=150, caption="Figure 1: System Architecture Diagram")

    pdf.ln(2)
    pdf.chapter_title("6", "Design Diagrams")
    pdf.section_title("6.1 Workflow Diagram")
    pdf.body_text(
        "The workflow diagram below shows the steps followed when a user runs a command: from input validation and image loading, "
        "to running the algorithm and saving the output images or 3D files."
    )
    pdf.add_figure("docs/diagrams/workflow_diagram.png", w=150, caption="Figure 2: Process Workflow Diagram")

    pdf.add_page()
    pdf.section_title("6.2 Use Case Diagram")
    pdf.body_text("The use case diagram illustrates the main actions a student or user can perform using the CLI toolkit.")
    pdf.add_figure("docs/diagrams/usecase_diagram.png", w=145, caption="Figure 3: Use Case Diagram")

    pdf.ln(2)
    pdf.section_title("6.3 Class and Component Diagram")
    pdf.body_text("The diagram below shows the package layout and the main functions implemented across each module.")
    pdf.add_figure("docs/diagrams/class_diagram.png", w=150, caption="Figure 4: Component and Package Structure")

    pdf.add_page()
    pdf.section_title("6.4 Sequence Diagram")
    pdf.body_text("The sequence diagram illustrates how the stereo reconstruction command executes from CLI input to 3D point cloud generation.")
    pdf.add_figure("docs/diagrams/sequence_diagram.png", w=150, caption="Figure 5: Sequence Diagram for Stereo Reconstruction")

    # ----------------------------------------------------
    # 7. DESIGN DECISIONS & RATIONALE
    # ----------------------------------------------------
    pdf.chapter_title("7", "Design Decisions & Rationale")
    pdf.bullet_point("Simple Code Style", "I chose to keep the functions straightforward and easy to understand with readable variable names and clear logic, rather than using complex classes or unnecessary layers of abstraction.")
    pdf.bullet_point("Standard Argparse", "Using Python's built-in argparse ensures that the CLI works right away on any computer without requiring extra heavy frameworks.")
    pdf.bullet_point("StereoSGBM for Depth", "I used Semi-Global Block Matching (SGBM) instead of basic Block Matching because SGBM handles smooth regions much better and produces cleaner disparity maps.")
    pdf.bullet_point("Standard PLY Format", "The 3D point cloud is saved in standard ASCII PLY format so that it can be easily opened in 3D tools like MeshLab or Blender.")
    pdf.bullet_point("Lambertian Model", "For photometric stereo, the Lambertian reflectance assumption makes it possible to solve for surface normals directly using simple linear least squares.")

    # ----------------------------------------------------
    # 8. IMPLEMENTATION DETAILS
    # ----------------------------------------------------
    pdf.add_page()
    pdf.chapter_title("8", "Implementation Details")
    pdf.body_text(
        "The project is structured into clean Python packages inside the visionforge directory:"
    )
    pdf.bullet_point("visionforge.common", "Contains io_utils.py for loading/saving images and writing .ply point cloud files, and metrics.py for calculating PSNR, MSE, and Entropy.")
    pdf.bullet_point("visionforge.lowlevel", "Contains filters.py (box blur, Gaussian blur, Laplacian), frequency.py (2D FFT and lowpass/highpass filtering), transforms.py (rotation, translation, affine, perspective), and histogram.py (histogram equalization and CLAHE).")
    pdf.bullet_point("visionforge.features", "Contains edges_corners.py (Canny, Harris, Hough lines), descriptors.py (SIFT and ORB matching), pyramids.py (Gaussian and Laplacian pyramids), and segmentation.py (Otsu thresholding, K-Means clustering, region growing).")
    pdf.bullet_point("visionforge.stereo_3d", "Contains epipolar.py (Fundamental matrix and epipolar lines), depth_reconstruction.py (disparity estimation using StereoSGBM and 3D triangulation), and rectification.py (homography stitching).")
    pdf.bullet_point("visionforge.motion_pattern", "Contains background_sub.py (frame differencing and MOG2), optical_flow.py (dense Farneback flow and sparse Lucas-Kanade), and dimensionality.py (PCA image compression).")
    pdf.bullet_point("visionforge.shape_from_x", "Contains photometric_stereo.py which calculates normal vectors and albedo using least squares and integrates surface gradients into a depth map.")

    # ----------------------------------------------------
    # 9. RESULTS & SCREENSHOTS
    # ----------------------------------------------------
    pdf.chapter_title("9", "Screenshots and Results")
    pdf.body_text("Below are sample visual results generated by running each module on test images:")
    
    pdf.section_title("9.1 Low-Level Processing & Filtering")
    pdf.add_figure("docs/figures/fig_lowlevel.png", w=155, caption="Figure 6: Original vs Gaussian Blur, 2D FFT Spectrum, and CLAHE Enhanced Image")

    pdf.add_page()
    pdf.section_title("9.2 Feature Detection & Image Segmentation")
    pdf.add_figure("docs/figures/fig_features.png", w=155, caption="Figure 7: Canny Edges, Harris Corners, Otsu Threshold, and K-Means Segmentation")

    pdf.ln(2)
    pdf.section_title("9.3 Stereo Disparity Estimation")
    pdf.add_figure("docs/figures/fig_stereo.png", w=145, caption="Figure 8: Stereo Pair (Left and Right) and Computed Disparity Map")

    pdf.add_page()
    pdf.section_title("9.4 Motion Analysis & Optical Flow")
    pdf.add_figure("docs/figures/fig_motion.png", w=145, caption="Figure 9: Motion Frames and Dense Optical Flow (HSV Visualization)")

    pdf.ln(2)
    pdf.section_title("9.5 Photometric Stereo 3D Surface Reconstruction")
    pdf.add_figure("docs/figures/fig_shape.png", w=155, caption="Figure 10: Multi-Light Illumination, Recovered Normals, Albedo, and 3D Depth Map")

    # ----------------------------------------------------
    # 10. TESTING APPROACH & 11. CHALLENGES FACED
    # ----------------------------------------------------
    pdf.add_page()
    pdf.chapter_title("10", "Testing Approach")
    pdf.body_text(
        "To test the project, I wrote automated unit tests using pytest. Each test file verifies that the algorithms "
        "produce outputs with correct dimensions, data types, and expected numerical values."
    )
    
    # Table of tests
    pdf.set_font("Times", "B", 10)
    pdf.cell(50, 7, "Test File", 1, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(55, 7, "Functions Tested", 1, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(45, 7, "Verification Criteria", 1, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(25, 7, "Status", 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    
    pdf.set_font("Times", "", 10)
    test_rows = [
        ("test_lowlevel.py", "Filters, FFT, Transforms, Hist", "Valid shapes, finite PSNR/entropy", "PASSED"),
        ("test_features.py", "Canny, Harris, Pyramids, Otsu", "Edge detection, level shapes", "PASSED"),
        ("test_stereo_3d.py", "Disparity, 3D Point Cloud", "Valid disparity, float coordinates", "PASSED"),
        ("test_motion_pattern.py", "Frame diff, Flow, PCA", "Flow shapes, PCA variance ratio", "PASSED"),
        ("test_shape_from_x.py", "Photometric Stereo, Depth", "Normalized vectors, valid depth", "PASSED")
    ]
    for file, funcs, crit, stat in test_rows:
        pdf.cell(50, 6, file, 1, new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(55, 6, funcs, 1, new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(45, 6, crit, 1, new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Times", "B", 10)
        pdf.cell(25, 6, stat, 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.set_font("Times", "", 10)
        
    pdf.ln(3)
    pdf.body_text("All 12 automated unit tests passed successfully on Windows 11 with Python 3.13.")

    pdf.ln(2)
    pdf.chapter_title("11", "Challenges Faced")
    pdf.bullet_point("Frequency Centering", "The raw 2D FFT output places zero frequency at the corners. I used np.fft.fftshift so that the low frequencies are centered properly before applying circular masks.")
    pdf.bullet_point("Stereo Block Matching Noise", "Basic stereo block matching had artifacts in flat regions. Tuning the SGBM parameters (smoothness penalties P1 and P2) solved this problem.")
    pdf.bullet_point("Depth Integration Edge Cases", "When integrating surface normals to compute depth, dividing by near-zero Nz values caused numerical spikes. Clamping Nz to a small minimum threshold prevented overflow.")

    # ----------------------------------------------------
    # 12. LEARNINGS, 13. FUTURE ENHANCEMENTS, 14. REFERENCES
    # ----------------------------------------------------
    pdf.chapter_title("12", "Learnings & Key Takeaways")
    pdf.bullet_point("Practical Understanding", "Implementing the syllabus algorithms helped me understand how mathematical concepts like 2D convolution, Fourier transforms, and matrix equations actually work on pixel values.")
    pdf.bullet_point("Geometric Vision", "Working with stereo images and photometric stereo showed me how multiple camera views or multiple lighting directions allow us to recover 3D information from 2D images.")
    pdf.bullet_point("Software Organization", "Structuring the code into clear modules with automated unit tests made the project much easier to debug and verify.")

    pdf.ln(2)
    pdf.chapter_title("13", "Future Enhancements")
    pdf.bullet_point("Real-time Webcam Support", "Adding a live video mode to track motion and optical flow in real time from a webcam.")
    pdf.bullet_point("3D Mesh Generation", "Connecting the 3D points from stereo reconstruction into a textured surface mesh.")
    pdf.bullet_point("Deep Learning Models", "Adding modern deep learning models for feature matching and depth estimation alongside the classical techniques.")

    pdf.ln(2)
    pdf.chapter_title("14", "References")
    pdf.body_text("1. Richard Szeliski, Computer Vision: Algorithms and Applications, 2nd Edition, Springer, 2022.")
    pdf.body_text("2. Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, Cambridge University Press, 2004.")
    pdf.body_text("3. Robert J. Woodham, Photometric method for determining surface orientation from multiple images, Optical Engineering, 1980.")
    pdf.body_text("4. OpenCV Open Source Computer Vision Library documentation (https://docs.opencv.org/).")

    pdf.output(output_path)
    print(f"Report PDF generated at: {output_path}")

if __name__ == "__main__":
    build_pdf()
