import cv2
import numpy as np

def compute_fundamental_matrix(pts1, pts2):
    F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_RANSAC)
    return F, mask

def draw_epipolar_lines(img1, img2, pts1, pts2):
    F, mask = compute_fundamental_matrix(pts1, pts2)
    if F is None or mask is None:
        return img1, img2
        
    pts1 = pts1[mask.ravel() == 1]
    pts2 = pts2[mask.ravel() == 1]
    
    lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1, 1, 2), 1, F)
    lines2 = lines2.reshape(-1, 3)
    
    out2 = img2.copy()
    if len(out2.shape) == 2:
        out2 = cv2.cvtColor(out2, cv2.COLOR_GRAY2BGR)
        
    w = img2.shape[1]
    for r, pt in zip(lines2, pts2):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r[2] / r[1]])
        x1, y1 = map(int, [w, -(r[2] + r[0] * w) / r[1]])
        cv2.line(out2, (x0, y0), (x1, y1), color, 1)
        cv2.circle(out2, (int(pt[0]), int(pt[1])), 4, color, -1)
        
    return out2, F
