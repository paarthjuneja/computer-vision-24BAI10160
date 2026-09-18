import cv2
import numpy as np

def detect_canny_edges(img, low_thresh=50, high_thresh=150):
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    return cv2.Canny(gray, low_thresh, high_thresh)

def detect_harris_corners(img, block_size=2, ksize=3, k=0.04, threshold=0.01):
    output = img.copy()
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
        output = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        
    gray_float = np.float32(gray)
    dst = cv2.cornerHarris(gray_float, block_size, ksize, k)
    dst = cv2.dilate(dst, None)
    
    output[dst > threshold * dst.max()] = [0, 0, 255]
    return output

def detect_hough_lines(img, threshold=100, min_line_length=50, max_line_gap=10):
    output = img.copy()
    if len(output.shape) == 2:
        output = cv2.cvtColor(output, cv2.COLOR_GRAY2BGR)
    edges = detect_canny_edges(img)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold, minLineLength=min_line_length, maxLineGap=max_line_gap)
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return output
