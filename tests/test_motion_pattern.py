import numpy as np
from visionforge.motion_pattern.background_sub import compute_frame_difference, BackgroundModel
from visionforge.motion_pattern.optical_flow import compute_dense_optical_flow
from visionforge.motion_pattern.dimensionality import compress_image_pca

def test_motion_difference():
    f1 = np.ones((50, 50), dtype=np.uint8) * 100
    f2 = f1.copy()
    f2[20:30, 20:30] = 200
    diff = compute_frame_difference(f1, f2, threshold=20)
    assert diff.shape == (50, 50)
    assert np.sum(diff) > 0

def test_optical_flow():
    f1 = np.ones((50, 50), dtype=np.uint8) * 100
    f2 = f1.copy()
    f2[10:20, 10:20] = 200
    vis, flow = compute_dense_optical_flow(f1, f2)
    assert vis.shape == (50, 50, 3)
    assert flow.shape == (50, 50, 2)

def test_pca():
    img = np.random.randint(0, 255, (40, 40), dtype=np.uint8)
    reconstructed, ratio = compress_image_pca(img, n_components=10)
    assert reconstructed.shape == (40, 40)
    assert 0.0 <= ratio <= 1.0
