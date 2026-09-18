import cv2
import numpy as np

def compute_disparity_map(img_left, img_right, num_disparities=64, block_size=15):
    if len(img_left.shape) == 3:
        gray_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)
        gray_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)
    else:
        gray_left = img_left
        gray_right = img_right
        
    stereo = cv2.StereoSGBM_create(
        minDisparity=0,
        numDisparities=num_disparities,
        blockSize=block_size,
        P1=8 * 3 * block_size ** 2,
        P2=32 * 3 * block_size ** 2,
        disp12MaxDiff=1,
        uniquenessRatio=10,
        speckleWindowSize=100,
        speckleRange=32
    )
    
    disparity = stereo.compute(gray_left, gray_right).astype(np.float32) / 16.0
    return disparity

def disparity_to_point_cloud(disparity, img_color=None, focal_length=800.0, baseline=0.1):
    h, w = disparity.shape
    cx = w / 2.0
    cy = h / 2.0
    
    points = []
    colors = []
    
    for v in range(0, h, 2):
        for u in range(0, w, 2):
            d = disparity[v, u]
            if d > 1.0:
                z = (focal_length * baseline) / d
                x = (u - cx) * z / focal_length
                y = (v - cy) * z / focal_length
                points.append([x, y, z])
                if img_color is not None:
                    b, g, r = img_color[v, u]
                    colors.append([r, g, b])
                else:
                    colors.append([200, 200, 200])
                    
    return np.array(points, dtype=np.float32), np.array(colors, dtype=np.uint8)
