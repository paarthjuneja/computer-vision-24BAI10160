import os
import cv2
import numpy as np

def load_image(path, as_gray=False):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {path}")
    if as_gray:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"Could not read image: {path}")
    return img

def save_image(path, img):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    cv2.imwrite(path, img)

def save_point_cloud_ply(path, points, colors=None):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    n = len(points)
    with open(path, "w") as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {n}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        if colors is not None:
            f.write("property uchar red\n")
            f.write("property uchar green\n")
            f.write("property uchar blue\n")
        f.write("end_header\n")
        
        for i in range(n):
            x, y, z = points[i]
            if colors is not None:
                r, g, b = colors[i]
                f.write(f"{x:.4f} {y:.4f} {z:.4f} {int(r)} {int(g)} {int(b)}\n")
            else:
                f.write(f"{x:.4f} {y:.4f} {z:.4f}\n")
