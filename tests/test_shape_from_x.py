import numpy as np
from visionforge.shape_from_x.photometric_stereo import compute_photometric_stereo, integrate_normals_to_depth

def test_photometric_stereo():
    h, w = 30, 30
    # Create 3 images under 3 different light directions
    img1 = np.ones((h, w), dtype=np.uint8) * 150
    img2 = np.ones((h, w), dtype=np.uint8) * 120
    img3 = np.ones((h, w), dtype=np.uint8) * 180
    
    lights = [
        [0.0, 0.5, 0.8],
        [0.5, 0.0, 0.8],
        [-0.5, 0.0, 0.8]
    ]
    
    normals, albedo, vis_normals = compute_photometric_stereo([img1, img2, img3], lights)
    assert normals.shape == (h, w, 3)
    assert albedo.shape == (h, w)
    assert vis_normals.shape == (h, w, 3)
    
    depth, vis_depth = integrate_normals_to_depth(normals)
    assert depth.shape == (h, w)
    assert vis_depth.shape == (h, w)
