import os
import cv2
import numpy as np

def generate_sample_images(output_dir="data"):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Base test image with geometric shapes
    img = np.ones((256, 256, 3), dtype=np.uint8) * 240
    cv2.circle(img, (80, 80), 40, (50, 100, 220), -1)
    cv2.rectangle(img, (140, 60), (220, 140), (80, 180, 60), -1)
    cv2.putText(img, "VisionForge", (30, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (20, 20, 20), 2)
    cv2.line(img, (20, 220), (236, 220), (120, 120, 120), 2)
    cv2.imwrite(os.path.join(output_dir, "input_sample.png"), img)
    
    # 2. Stereo pair (left and right with horizontal shift for foreground)
    left = np.ones((200, 300, 3), dtype=np.uint8) * 230
    cv2.rectangle(left, (20, 20), (280, 180), (200, 200, 200), 2)
    cv2.rectangle(left, (110, 50), (190, 150), (40, 60, 200), -1)
    cv2.circle(left, (150, 100), 25, (255, 255, 255), -1)
    
    right = np.ones((200, 300, 3), dtype=np.uint8) * 230
    cv2.rectangle(right, (20, 20), (280, 180), (200, 200, 200), 2)
    # Disparity shift of 16 pixels to the left
    cv2.rectangle(right, (94, 50), (174, 150), (40, 60, 200), -1)
    cv2.circle(right, (134, 100), 25, (255, 255, 255), -1)
    
    cv2.imwrite(os.path.join(output_dir, "stereo_left.png"), left)
    cv2.imwrite(os.path.join(output_dir, "stereo_right.png"), right)
    
    # 3. Motion pair (frame 1 and frame 2)
    f1 = np.ones((200, 250, 3), dtype=np.uint8) * 220
    cv2.rectangle(f1, (50, 80), (100, 130), (30, 40, 180), -1)
    
    f2 = np.ones((200, 250, 3), dtype=np.uint8) * 220
    cv2.rectangle(f2, (80, 80), (130, 130), (30, 40, 180), -1)
    
    cv2.imwrite(os.path.join(output_dir, "motion_frame1.png"), f1)
    cv2.imwrite(os.path.join(output_dir, "motion_frame2.png"), f2)
    
    # 4. Photometric stereo sphere images (4 light sources)
    h, w = 150, 150
    center_x, center_y = w // 2, h // 2
    radius = 50.0
    
    y, x = np.mgrid[:h, :w]
    dist_sq = (x - center_x) ** 2 + (y - center_y) ** 2
    mask = dist_sq <= (radius ** 2)
    
    nx = np.zeros((h, w), dtype=np.float32)
    ny = np.zeros((h, w), dtype=np.float32)
    nz = np.zeros((h, w), dtype=np.float32)
    
    nz[mask] = np.sqrt(np.maximum(0.0, radius ** 2 - dist_sq[mask])) / radius
    nx[mask] = (x - center_x)[mask] / radius
    ny[mask] = (y - center_y)[mask] / radius
    
    lights = [
        [0.0, 0.577, 0.816],
        [0.577, 0.0, 0.816],
        [0.0, -0.577, 0.816],
        [-0.577, 0.0, 0.816]
    ]
    
    for idx, light in enumerate(lights):
        dot = nx * light[0] + ny * light[1] + nz * light[2]
        intensity = np.maximum(0.0, dot) * mask
        img_light = (intensity * 255.0).astype(np.uint8)
        cv2.imwrite(os.path.join(output_dir, f"light{idx + 1}.png"), img_light)
        
    print(f"Sample images successfully generated in '{output_dir}'.")


if __name__ == "__main__":
    generate_sample_images()
