import cv2
import numpy as np

def rotate_image(img, angle):
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(img, matrix, (w, h))

def translate_image(img, dx, dy):
    h, w = img.shape[:2]
    matrix = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(img, matrix, (w, h))

def apply_affine_transform(img, pts1=None, pts2=None):
    h, w = img.shape[:2]
    if pts1 is None:
        pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
    if pts2 is None:
        pts2 = np.float32([[10, 100], [200, 50], [100, 250]])
    matrix = cv2.getAffineTransform(pts1, pts2)
    return cv2.warpAffine(img, matrix, (w, h))

def apply_perspective_transform(img, pts1=None, pts2=None):
    h, w = img.shape[:2]
    if pts1 is None:
        pts1 = np.float32([[0, 0], [w - 1, 0], [0, h - 1], [w - 1, h - 1]])
    if pts2 is None:
        pts2 = np.float32([[20, 30], [w - 40, 20], [40, h - 20], [w - 20, h - 40]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    return cv2.warpPerspective(img, matrix, (w, h))
