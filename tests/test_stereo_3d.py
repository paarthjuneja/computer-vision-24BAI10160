import numpy as np
from visionforge.stereo_3d.depth_reconstruction import compute_disparity_map, disparity_to_point_cloud
from visionforge.stereo_3d.epipolar import compute_fundamental_matrix

def test_disparity_and_cloud():
    left = np.ones((80, 80), dtype=np.uint8) * 128
    right = np.ones((80, 80), dtype=np.uint8) * 128
    left[20:60, 20:60] = 200
    right[20:60, 15:55] = 200
    
    disp = compute_disparity_map(left, right, num_disparities=16, block_size=5)
    assert disp.shape == (80, 80)
    
    points, colors = disparity_to_point_cloud(disp, focal_length=100.0, baseline=0.1)
    assert isinstance(points, np.ndarray)
    assert isinstance(colors, np.ndarray)
