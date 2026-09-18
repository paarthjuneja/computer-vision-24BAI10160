import cv2
import numpy as np

def segment_otsu(img):
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def segment_kmeans(img, k=3):
    pixel_vals = img.reshape((-1, 3))
    pixel_vals = np.float32(pixel_vals)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(pixel_vals, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    segmented = centers[labels.flatten()]
    return segmented.reshape(img.shape)

def segment_region_growing(img, seed=(50, 50), threshold=15):
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
        
    h, w = gray.shape
    visited = np.zeros((h, w), dtype=np.uint8)
    segmented = np.zeros((h, w), dtype=np.uint8)
    
    sy, sx = seed
    if sy >= h or sx >= w:
        sy, sx = h // 2, w // 2
    seed_val = float(gray[sy, sx])
    
    queue = [(sy, sx)]
    visited[sy, sx] = 1
    segmented[sy, sx] = 255
    
    while len(queue) > 0:
        y, x = queue.pop(0)
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                visited[ny, nx] = 1
                diff = abs(float(gray[ny, nx]) - seed_val)
                if diff <= threshold:
                    segmented[ny, nx] = 255
                    queue.append((ny, nx))
                    
    return segmented
