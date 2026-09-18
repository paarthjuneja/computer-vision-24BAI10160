import cv2
import numpy as np

def apply_box_blur(img, ksize=5):
    return cv2.blur(img, (ksize, ksize))

def apply_gaussian_blur(img, ksize=5, sigma=1.0):
    if ksize % 2 == 0:
        ksize += 1
    return cv2.GaussianBlur(img, (ksize, ksize), sigma)

def apply_bilateral_filter(img, d=9, sigma_color=75, sigma_space=75):
    return cv2.bilateralFilter(img, d, sigma_color, sigma_space)

def apply_laplacian(img):
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    lap = np.uint8(np.absolute(lap))
    return lap
