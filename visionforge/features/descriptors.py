import cv2
import numpy as np

def extract_and_match_features(img1, img2, method="orb", max_features=500):
    if method == "sift":
        detector = cv2.SIFT_create(max_features)
        matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    else:
        detector = cv2.ORB_create(max_features)
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        
    kp1, des1 = detector.detectAndCompute(img1, None)
    kp2, des2 = detector.detectAndCompute(img2, None)
    
    if des1 is None or des2 is None or len(des1) == 0 or len(des2) == 0:
        h = max(img1.shape[0], img2.shape[0])
        w = img1.shape[1] + img2.shape[1]
        empty = np.zeros((h, w, 3), dtype=np.uint8)
        return empty, 0
        
    matches = matcher.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    matched_img = cv2.drawMatches(img1, kp1, img2, kp2, matches[:30], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    return matched_img, len(matches)
