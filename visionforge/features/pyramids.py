import cv2

def build_gaussian_pyramid(img, levels=3):
    pyramid = [img]
    current = img
    for _ in range(levels):
        current = cv2.pyrDown(current)
        pyramid.append(current)
    return pyramid

def build_laplacian_pyramid(img, levels=3):
    gaussian_pyr = build_gaussian_pyramid(img, levels)
    laplacian_pyr = []
    for i in range(levels):
        size = (gaussian_pyr[i].shape[1], gaussian_pyr[i].shape[0])
        expanded = cv2.pyrUp(gaussian_pyr[i + 1], dstsize=size)
        lap = cv2.subtract(gaussian_pyr[i], expanded)
        laplacian_pyr.append(lap)
    laplacian_pyr.append(gaussian_pyr[-1])
    return laplacian_pyr
