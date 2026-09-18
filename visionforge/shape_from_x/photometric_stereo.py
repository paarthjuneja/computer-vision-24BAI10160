import cv2
import numpy as np

def compute_photometric_stereo(images, light_dirs):
    k = len(images)
    h, w = images[0].shape[:2]
    
    gray_imgs = []
    for img in images:
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        gray_imgs.append(gray.astype(np.float32) / 255.0)
        
    I = np.zeros((k, h * w), dtype=np.float32)
    for i in range(k):
        I[i, :] = gray_imgs[i].reshape(-1)
        
    L = np.array(light_dirs, dtype=np.float32)
    for i in range(k):
        norm = np.linalg.norm(L[i])
        if norm > 0:
            L[i] = L[i] / norm
            
    # G = (L^T L)^(-1) L^T I
    G, _, _, _ = np.linalg.lstsq(L, I, rcond=None)
    
    albedo = np.linalg.norm(G, axis=0)
    albedo_map = albedo.reshape((h, w))
    albedo_map = cv2.normalize(albedo_map, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    normals = np.zeros((3, h * w), dtype=np.float32)
    valid_mask = albedo > 1e-4
    normals[:, valid_mask] = G[:, valid_mask] / albedo[valid_mask]
    normals[:, ~valid_mask] = np.array([[0], [0], [1]])
    
    normal_map = normals.reshape((3, h, w)).transpose(1, 2, 0)
    
    # Map normal range [-1, 1] to [0, 255] for RGB visualization
    vis_normal = ((normal_map + 1.0) * 0.5 * 255.0).astype(np.uint8)
    return normal_map, albedo_map, vis_normal

def integrate_normals_to_depth(normal_map):
    h, w = normal_map.shape[:2]
    nx = normal_map[:, :, 0]
    ny = normal_map[:, :, 1]
    nz = normal_map[:, :, 2]
    
    nz_safe = np.where(np.abs(nz) < 0.1, 0.1, nz)
    p = -nx / nz_safe
    q = -ny / nz_safe
    
    depth = np.zeros((h, w), dtype=np.float32)
    for y in range(1, h):
        depth[y, 0] = depth[y - 1, 0] + q[y, 0]
    for y in range(h):
        for x in range(1, w):
            depth[y, x] = depth[y, x - 1] + p[y, x]
            
    vis_depth = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    return depth, vis_depth
