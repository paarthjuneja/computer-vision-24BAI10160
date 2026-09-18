import numpy as np
import cv2
from visionforge.features.edges_corners import detect_canny_edges, detect_harris_corners
from visionforge.features.pyramids import build_gaussian_pyramid
from visionforge.features.segmentation import segment_otsu, segment_kmeans

def test_canny_and_harris():
    img = np.zeros((80, 80), dtype=np.uint8)
    img[20:60, 20:60] = 255
    
    edges = detect_canny_edges(img)
    assert edges.shape == (80, 80)
    assert np.max(edges) > 0
    
    corners = detect_harris_corners(img)
    assert corners.shape == (80, 80, 3)

def test_pyramids():
    img = np.ones((64, 64, 3), dtype=np.uint8) * 100
    pyr = build_gaussian_pyramid(img, levels=2)
    assert len(pyr) == 3
    assert pyr[1].shape == (32, 32, 3)
    assert pyr[2].shape == (16, 16, 3)

def test_segmentation():
    img = np.zeros((60, 60, 3), dtype=np.uint8)
    img[:30, :] = 200
    
    otsu = segment_otsu(img)
    assert otsu.shape == (60, 60)
    
    kmeans_seg = segment_kmeans(img, k=2)
    assert kmeans_seg.shape == img.shape
