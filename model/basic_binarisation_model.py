import numpy as np
import pygame
from PIL import Image
from PIL.ImageOps import grayscale
from math import log2
from scipy.ndimage import uniform_filter, minimum_filter, maximum_filter

class BasicBinarisationModel:
    def __init__(self):
        pass

    def percent_black_selection(self, image_surface, percent=50):
        image_array = pygame.surfarray.array3d(image_surface)
        grayscale_image = self._to_grayscale(image_array)
        flat = grayscale_image.flatten()
        threshold_index = int(len(flat) * (percent / 100.0))
        sorted_pixels = np.sort(flat)
        threshold = sorted_pixels[threshold_index]

        binary_image = (grayscale_image < threshold) * 255
        return self._array_to_surface(binary_image)

    def mean_iterative_selection(self, image_surface, max_iterations=10):
        image_array = pygame.surfarray.array3d(image_surface)
        grayscale_image = self._to_grayscale(image_array)
        threshold = grayscale_image.mean()
        for _ in range(max_iterations):
            lower = grayscale_image[grayscale_image < threshold]
            upper = grayscale_image[grayscale_image >= threshold]
            new_threshold = (lower.mean() + upper.mean()) / 2
            if new_threshold == threshold:
                break
            threshold = new_threshold
        binary_image = (grayscale_image < threshold) * 255
        return self._array_to_surface(binary_image)

    def entropy_selection(self, image_surface):
        image_array = pygame.surfarray.array3d(image_surface)
        grayscale_image = self._to_grayscale(image_array)
        histogram, _ = np.histogram(grayscale_image, bins=256, range=(0, 255))
        total = grayscale_image.size

        histogram = histogram / total

        entropy = np.zeros(256)
        for t in range(256):
            p1 = histogram[:t]
            p2 = histogram[t:]
            p1 = p1[p1 > 0]
            p2 = p2[p2 > 0]
            entropy1 = -np.sum(p1 * np.log2(p1))
            entropy2 = -np.sum(p2 * np.log2(p2))
            entropy[t] = entropy1 + entropy2

        threshold = np.argmax(entropy)
        binary_image = (grayscale_image < threshold) * 255
        return self._array_to_surface(binary_image)

    def _to_grayscale(self, image_array):
        return (0.2989 * image_array[:, :, 0] + 
                0.5870 * image_array[:, :, 1] + 
                0.1140 * image_array[:, :, 2]).astype(np.uint8)

    def _array_to_surface(self, array):
        return pygame.surfarray.make_surface(np.stack([array]*3, axis=-1))

    def manual_threshold(self, image_surface, threshold=128):
        """Binaryzacja przy użyciu ręcznego progu."""
        image_array = pygame.surfarray.array3d(image_surface)
        grayscale_image = self._to_grayscale(image_array)
        binary_image = (grayscale_image < threshold) * 255
        return self._array_to_surface(binary_image)

    def otsu_threshold(self, image_surface):
        """Binaryzacja przy użyciu metody Otsu."""
        image_array = pygame.surfarray.array3d(image_surface)
        grayscale = self._to_grayscale(image_array)
        histogram, _ = np.histogram(grayscale, bins=256, range=(0, 255))
        total = grayscale.size

        current_max, threshold = 0, 0
        sum_total, sum_foreground = 0, 0
        weight_background, weight_foreground = 0, 0

        for t in range(256):
            sum_total += t * histogram[t]

        for t in range(256):
            weight_background += histogram[t]
            if weight_background == 0:
                continue
            weight_foreground = total - weight_background
            if weight_foreground == 0:
                break
            sum_foreground += t * histogram[t]
            mean_background = sum_foreground / weight_background
            mean_foreground = (sum_total - sum_foreground) / weight_foreground
            var_between = weight_background * weight_foreground * (mean_background - mean_foreground) ** 2
            if var_between > current_max:
                current_max = var_between
                threshold = t

        binary_image = (grayscale < threshold) * 255
        return self._array_to_surface(binary_image)

    def niblack_threshold(self, image_surface, window_size=15, k=-0.2):
        """Binaryzacja przy użyciu metody Niblacka."""
        image_array = pygame.surfarray.array3d(image_surface)
        grayscale = self._to_grayscale(image_array).astype(np.float32)
        mean = uniform_filter(grayscale, size=window_size, mode='reflect')
        mean_sq = uniform_filter(grayscale**2, size=window_size, mode='reflect')
        std = np.sqrt(mean_sq - mean**2)
        threshold = mean + k * std
        binary = (grayscale > threshold).astype(np.uint8) * 255
        return self._array_to_surface(binary)

    def sauvola_threshold(self, image_surface, window_size=15, k=0.5, R=128):
        """Binaryzacja przy użyciu metody Sauvola."""
        image_array = pygame.surfarray.array3d(image_surface)
        grayscale = self._to_grayscale(image_array).astype(np.float32)
        mean = uniform_filter(grayscale, size=window_size, mode='reflect')
        mean_sq = uniform_filter(grayscale**2, size=window_size, mode='reflect')
        std = np.sqrt(mean_sq - mean**2)
        threshold = mean * (1 + k * ((std / R) - 1))
        binary = (grayscale > threshold).astype(np.uint8) * 255
        return self._array_to_surface(binary)

    def bernsen_threshold(self, image_surface, window_size=15, contrast_threshold=15):
        """Binaryzacja przy użyciu metody Bernsena."""
        image_array = pygame.surfarray.array3d(image_surface)
        grayscale = self._to_grayscale(image_array)
        local_min = minimum_filter(grayscale, size=window_size, mode='reflect')
        local_max = maximum_filter(grayscale, size=window_size, mode='reflect')
        local_contrast = local_max - local_min
        threshold = (local_min + local_max) / 2
        binary = np.where(local_contrast < contrast_threshold, 255, 
                          np.where(grayscale > threshold, 255, 0)).astype(np.uint8)
        return self._array_to_surface(binary)
