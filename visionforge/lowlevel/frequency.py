import cv2
import numpy as np

def compute_fft_spectrum(img):
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    
    dft = np.fft.fft2(gray)
    dft_shift = np.fft.fftshift(dft)
    magnitude = 20 * np.log(np.abs(dft_shift) + 1)
    return cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

def apply_frequency_filter(img, filter_type="lowpass", radius=30):
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
        
    rows, cols = gray.shape
    crow, ccol = rows // 2, cols // 2
    
    dft = np.fft.fft2(gray)
    dft_shift = np.fft.fftshift(dft)
    
    mask = np.zeros((rows, cols), np.float32)
    y, x = np.ogrid[:rows, :cols]
    dist = np.sqrt((x - ccol) ** 2 + (y - crow) ** 2)
    
    if filter_type == "lowpass":
        mask[dist <= radius] = 1
    elif filter_type == "highpass":
        mask[dist > radius] = 1
    else:
        mask = np.ones((rows, cols), np.float32)
        
    filtered_shift = dft_shift * mask
    f_ishift = np.fft.ifftshift(filtered_shift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    
    return np.clip(img_back, 0, 255).astype(np.uint8)
