import numpy as np
import pygame
import cv2

class HistogramModel:
    def __init__(self):
        pass

    def stretch_histogram(self, image):
        arr = pygame.surfarray.array3d(image).astype(float)
        print(f"Original array shape: {arr.shape}, dtype: {arr.dtype}")
        print(f"Original array min: {arr.min()}, max: {arr.max()}")

        stretched_arr = self._stretch_array(arr)
        print(f"Stretched array min: {stretched_arr.min()}, max: {stretched_arr.max()}")


        stretched_arr = stretched_arr.astype(np.uint8)
        
        stretched_image = pygame.surfarray.make_surface(stretched_arr)
        return stretched_image

    def equalize_histogram(self, image):
        arr = pygame.surfarray.array3d(image)
        print(f"Original array shape: {arr.shape}, dtype: {arr.dtype}")
        equalized_arr = self._equalize_array(arr)
        print(f"Equalized array min: {equalized_arr.min()}, max: {equalized_arr.max()}")
        equalized_image = pygame.surfarray.make_surface(equalized_arr)
        return equalized_image

    def _stretch_array(self, arr):
        """
        Rozszerzenie histogramu dla każdego kanału RGB przy użyciu wektorowych operacji NumPy.
        """
        # Oblicz minimalne i maksymalne wartości dla każdego kanału
        min_vals = arr.min(axis=(0, 1), keepdims=True)
        max_vals = arr.max(axis=(0, 1), keepdims=True)

        print(f"Min values per channel: {min_vals.flatten()}")
        print(f"Max values per channel: {max_vals.flatten()}")


        scale = 255 / (max_vals - min_vals)
        scale[np.isinf(scale)] = 1  # Jeśli max_val == min_val, ustaw skalę na 1


        stretched = (arr - min_vals) * scale


        stretched = np.clip(stretched, 0, 255)

        print(f"After stretching, array min: {stretched.min()}, max: {stretched.max()}")

        return stretched

    def _equalize_array(self, arr):
        """
        Wyrównanie histogramu dla każdego kanału RGB.
        """
        equalized = np.zeros_like(arr)
        for i in range(3):  # RGB
            channel = arr[:, :, i]
            hist, bins = np.histogram(channel.flatten(), 256, [0, 256])
            cdf = hist.cumsum()
            cdf_normalized = cdf * 255 / cdf[-1]  # Normalizacja


            equalized_channel = np.interp(channel.flatten(), bins[:-1], cdf_normalized)
            equalized[:, :, i] = equalized_channel.reshape(channel.shape).astype(np.uint8)
        return equalized


    def stretch_histogram_cv2(self, image):
        """
        Rozszerza histogram obrazu używając OpenCV.
        """

        arr = pygame.surfarray.array3d(image)

        arr = np.transpose(arr, (1, 0, 2))
        print(f"[cv2] Original array shape: {arr.shape}, dtype: {arr.dtype}")


        arr_bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


        stretched_bgr = cv2.normalize(arr_bgr, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

        print(f"[cv2] Stretched array min: {stretched_bgr.min()}, max: {stretched_bgr.max()}")


        stretched_rgb = cv2.cvtColor(stretched_bgr, cv2.COLOR_BGR2RGB)


        stretched_rgb = np.transpose(stretched_rgb, (1, 0, 2)).astype(np.uint8)


        stretched_surface = pygame.surfarray.make_surface(stretched_rgb)

        return stretched_surface

    def stretch_histogram_numpy(self, image):
        """
        Rozszerza histogram obrazu używając tylko NumPy.
        """

        arr = pygame.surfarray.array3d(image).astype(float)

        arr = np.transpose(arr, (1, 0, 2))
        print(f"[NumPy] Original array shape: {arr.shape}, dtype: {arr.dtype}")
        print(f"[NumPy] Original array min: {arr.min()}, max: {arr.max()}")


        min_vals = arr.min(axis=(0, 1), keepdims=True)
        max_vals = arr.max(axis=(0, 1), keepdims=True)

        print(f"[NumPy] Min values per channel: {min_vals.flatten()}")
        print(f"[NumPy] Max values per channel: {max_vals.flatten()}")


        scale = 255 / (max_vals - min_vals)
        scale[np.isinf(scale)] = 1 


        stretched = (arr - min_vals) * scale

        stretched = np.clip(stretched, 0, 255)

        print(f"[NumPy] After stretching, array min: {stretched.min()}, max: {stretched.max()}")

        stretched = stretched.astype(np.uint8)

        stretched = np.transpose(stretched, (1, 0, 2))

        stretched_surface = pygame.surfarray.make_surface(stretched)

        return stretched_surface
