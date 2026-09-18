import numpy as np
from sklearn.decomposition import PCA

def apply_pca(data_matrix, n_components=5):
    pca = PCA(n_components=n_components)
    transformed = pca.fit_transform(data_matrix)
    reconstructed = pca.inverse_transform(transformed)
    explained_ratio = pca.explained_variance_ratio_
    return transformed, reconstructed, explained_ratio

def compress_image_pca(gray_img, n_components=20):
    h, w = gray_img.shape
    n = min(n_components, h, w)
    pca = PCA(n_components=n)
    transformed = pca.fit_transform(gray_img)
    reconstructed = pca.inverse_transform(transformed)
    return np.clip(reconstructed, 0, 255).astype(np.uint8), float(np.sum(pca.explained_variance_ratio_))
