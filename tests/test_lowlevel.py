import numpy as np
import cv2
from visionforge.lowlevel.filters import apply_box_blur, apply_gaussian_blur, apply_laplacian
from visionforge.lowlevel.frequency import compute_fft_spectrum, apply_frequency_filter
from visionforge.lowlevel.transforms import rotate_image, translate_image
from visionforge.lowlevel.histogram import equalize_histogram, apply_clahe
from visionforge.common.metrics import calculate_mse, calculate_psnr

def test_filters():
    img = np.ones((50, 50, 3), dtype=np.uint8) * 100
    blur = apply_box_blur(img, ksize=3)
    assert blur.shape == img.shape
    
    gauss = apply_gaussian_blur(img, ksize=3)
    assert gauss.shape == img.shape
    
    lap = apply_laplacian(img)
    assert lap.shape == (50, 50)

def test_frequency():
    img = np.zeros((64, 64), dtype=np.uint8)
    img[20:40, 20:40] = 255
    spectrum = compute_fft_spectrum(img)
    assert spectrum.shape == (64, 64)
    
    lowpass = apply_frequency_filter(img, "lowpass", radius=10)
    assert lowpass.shape == (64, 64)

def test_transforms():
    img = np.ones((40, 40, 3), dtype=np.uint8) * 128
    rotated = rotate_image(img, 90)
    assert rotated.shape == img.shape
    
    translated = translate_image(img, 5, 5)
    assert translated.shape == img.shape

def test_histogram():
    img = np.ones((50, 50), dtype=np.uint8) * 50
    eq = equalize_histogram(img)
    assert eq.shape == img.shape
    
    clahe_img = apply_clahe(img)
    assert clahe_img.shape == img.shape
