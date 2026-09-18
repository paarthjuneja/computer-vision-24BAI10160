import numpy as np

def calculate_mse(img1, img2):
    diff = img1.astype(float) - img2.astype(float)
    return float(np.mean(diff ** 2))

def calculate_psnr(img1, img2):
    mse = calculate_mse(img1, img2)
    if mse == 0:
        return 100.0
    max_pixel = 255.0
    return float(20 * np.log10(max_pixel / np.sqrt(mse)))

def calculate_entropy(img):
    if len(img.shape) == 3:
        gray = np.mean(img, axis=2).astype(np.uint8)
    else:
        gray = img
    hist, _ = np.histogram(gray, bins=256, range=(0, 256))
    prob = hist / hist.sum()
    prob = prob[prob > 0]
    return float(-np.sum(prob * np.log2(prob)))
