import cv2
import numpy as np

def compute_frame_difference(frame1, frame2, threshold=30):
    if len(frame1.shape) == 3:
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    else:
        gray1 = frame1
        
    if len(frame2.shape) == 3:
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    else:
        gray2 = frame2
        
    diff = cv2.absdiff(gray1, gray2)
    _, mask = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    return mask

class BackgroundModel:
    def __init__(self, history=500, var_threshold=16, detect_shadows=True):
        self.subtractor = cv2.createBackgroundSubtractorMOG2(
            history=history,
            varThreshold=var_threshold,
            detectShadows=detect_shadows
        )

    def apply(self, frame):
        return self.subtractor.apply(frame)
