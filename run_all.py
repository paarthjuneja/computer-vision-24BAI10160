import subprocess
import sys

def main():
    print("=" * 60)
    print(" VisionForge: Running Full Project Demo & Verification")
    print("=" * 60)
    
    # 1. Generate sample data
    print("\n[1/3] Generating synthetic datasets...")
    subprocess.run([sys.executable, "data/generate_samples.py"], check=True)
    
    # 2. Run unit tests
    print("\n[2/3] Running automated unit tests (pytest)...")
    result = subprocess.run([sys.executable, "-m", "pytest", "-v"])
    if result.returncode != 0:
        print("Unit tests failed.")
        return
        
    # 3. Test CLI commands
    print("\n[3/3] Running CLI smoke tests across modules...")
    commands = [
        [sys.executable, "-m", "visionforge.cli", "lowlevel", "-i", "data/input_sample.png", "-o", "output/demo_blur.png", "-a", "gaussian"],
        [sys.executable, "-m", "visionforge.cli", "features", "-i", "data/input_sample.png", "-o", "output/demo_canny.png", "-a", "canny"],
        [sys.executable, "-m", "visionforge.cli", "stereo", "-l", "data/stereo_left.png", "-r", "data/stereo_right.png", "-o", "output/demo_disp.png", "--ply", "output/demo_points.ply"],
        [sys.executable, "-m", "visionforge.cli", "motion", "-f1", "data/motion_frame1.png", "-f2", "data/motion_frame2.png", "-o", "output/demo_flow.png", "-a", "dense_flow"],
        [sys.executable, "-m", "visionforge.cli", "shape", "-i", "data/light1.png", "data/light2.png", "data/light3.png", "data/light4.png", "-o", "output/demo_normals.png"]
    ]
    for cmd in commands:
        subprocess.run(cmd, check=True)
        
    print("\n" + "=" * 60)
    print(" All demos, tests, and CLI modules verified successfully!")
    print(" Output files saved to 'output/' directory.")
    print("=" * 60)

if __name__ == "__main__":
    main()
