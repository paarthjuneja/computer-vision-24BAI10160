import cv2
import numpy as np

def compute_dense_optical_flow(prev_frame, curr_frame):
    if len(prev_frame.shape) == 3:
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    else:
        prev_gray = prev_frame
        
    if len(curr_frame.shape) == 3:
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
    else:
        curr_gray = curr_frame
        
    flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    
    hsv = np.zeros((prev_gray.shape[0], prev_gray.shape[1], 3), dtype=np.uint8)
    hsv[..., 1] = 255
    
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    
    bgr_flow = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bgr_flow, flow

def compute_sparse_optical_flow(prev_frame, curr_frame, max_corners=100):
    if len(prev_frame.shape) == 3:
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        out = curr_frame.copy()
    else:
        prev_gray = prev_frame
        out = cv2.cvtColor(curr_frame, cv2.COLOR_GRAY2BGR)
        
    if len(curr_frame.shape) == 3:
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
    else:
        curr_gray = curr_frame
        
    p0 = cv2.goodFeaturesToTrack(prev_gray, maxCorners=max_corners, qualityLevel=0.3, minDistance=7)
    if p0 is None:
        return out, 0
        
    p1, st, err = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, p0, None)
    
    good_new = p1[st == 1]
    good_old = p0[st == 1]
    
    for new, old in zip(good_new, good_old):
        a, b = map(int, new.ravel())
        c, d = map(int, old.ravel())
        cv2.line(out, (a, b), (c, d), (0, 255, 0), 2)
        cv2.circle(out, (a, b), 4, (0, 0, 255), -1)
        
    return out, len(good_new)
