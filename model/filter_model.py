# filter_model.py

import numpy as np
import pygame.surfarray as surfarray
import pygame
from scipy.ndimage import convolve, median_filter
from numpy.lib.stride_tricks import sliding_window_view



class FilterModel:
    def apply_smoothing_filter(self, image):
        array = surfarray.array3d(image).astype(np.float32)
        array = np.transpose(array, (1, 0, 2))  
        
        kernel = np.ones((3, 3)) / 9.0
        
        filtered_array = np.empty_like(array)
        for c in range(3):
            filtered_array[:, :, c] = convolve(array[:, :, c], kernel, mode='nearest')
        
        filtered_array = np.clip(filtered_array, 0, 255).astype(np.uint8)
        filtered_image = pygame.surfarray.make_surface(np.transpose(filtered_array, (1, 0, 2)))
        return filtered_image

    def apply_median_filter(self, image):
        """
        za wolna funkca
        """
        array = surfarray.array3d(image).astype(np.float32)
        array = np.transpose(array, (1, 0, 2))

        padded_array = np.pad(array, ((1,1), (1,1), (0,0)), mode='edge')

        filtered_array = np.empty_like(array)

        for y in range(array.shape[0]):
            for x in range(array.shape[1]):
                for c in range(3):
                    window = padded_array[y:y+3, x:x+3, c]
                    median = np.median(window)
                    filtered_array[y, x, c] = median

        filtered_array = np.clip(filtered_array, 0, 255).astype(np.uint8)
        filtered_image = pygame.surfarray.make_surface(np.transpose(filtered_array, (1, 0, 2)))  
        return filtered_image

    def apply_median_filter_scipy(self, image):
        """
        testowa funkcja nie używana w programie 
        """
        array = surfarray.array3d(image).astype(np.float32)
        array = np.transpose(array, (1, 0, 2))  # [height][width][3]

        filtered_array = np.empty_like(array)
        for c in range(3):
            filtered_array[:, :, c] = median_filter(array[:, :, c], size=3, mode='nearest')

        filtered_array = np.clip(filtered_array, 0, 255).astype(np.uint8)
        filtered_image = pygame.surfarray.make_surface(np.transpose(filtered_array, (1, 0, 2)))  
        return filtered_image

    def apply_median_filter_numpy(self, image):
        """
        funkcja używana w programie
        """
        array = surfarray.array3d(image).astype(np.float32)
        array = np.transpose(array, (1, 0, 2))  # [height][width][3]

        padded_array = np.pad(array, ((1, 1), (1, 1), (0, 0)), mode='edge')

        filtered_array = np.empty_like(array)

        try:
            from numpy.lib.stride_tricks import sliding_window_view
        except ImportError:
            raise ImportError("Your NumPy version does not support sliding_window_view. Please update NumPy to >=1.20.")

        for c in range(3):
            channel = padded_array[:, :, c]  # [height+2, width+2]
            windows = sliding_window_view(channel, (3, 3))  # [height, width, 3, 3]

            median = np.median(windows, axis=(2, 3))

            filtered_array[:, :, c] = median

        filtered_array = np.clip(filtered_array, 0, 255).astype(np.uint8)
        filtered_image = pygame.surfarray.make_surface(np.transpose(filtered_array, (1, 0, 2)))  # [width][height][3]
        return filtered_image


    def apply_sobel_filter_numpy(self, image):
        """
        Zastosuj filtr Sobela (wykrywanie krawędzi) na obrazie za pomocą NumPy w sposób wektorowy.
        """
        array = surfarray.array3d(image).astype(np.float32)
        array = np.transpose(array, (1, 0, 2))  # [height][width][3]

        padded_array = np.pad(array, ((1, 1), (1, 1), (0, 0)), mode='edge')

        sobel_x = np.array([[ -1, 0, 1],
                            [ -2, 0, 2],
                            [ -1, 0, 1]], dtype=np.float32)

        sobel_y = np.array([[ -1, -2, -1],
                            [  0,  0,  0],
                            [  1,  2,  1]], dtype=np.float32)

        filtered_array = np.empty_like(array)

        try:
            from numpy.lib.stride_tricks import sliding_window_view
        except ImportError:
            raise ImportError("Your NumPy version does not support sliding_window_view. Please update NumPy to >=1.20.")

        for c in range(3):
            channel = padded_array[:, :, c]  # [height+2, width+2]
            windows = sliding_window_view(channel, (3, 3))  # [height, width, 3, 3]

            gx = np.sum(windows * sobel_x, axis=(2, 3))
            gy = np.sum(windows * sobel_y, axis=(2, 3))

            gradient_magnitude = np.sqrt(gx**2 + gy**2)

            gradient_magnitude = np.clip(gradient_magnitude, 0, 255)

            filtered_array[:, :, c] = gradient_magnitude

        filtered_array = np.clip(filtered_array, 0, 255).astype(np.uint8)
        filtered_image = pygame.surfarray.make_surface(np.transpose(filtered_array, (1, 0, 2)))  # [width][height][3]
        return filtered_image


    def apply_high_pass_filter_numpy(self, image):
        """
        Zastosuj filtr górnoprzepustowy (wyostrzający) na obrazie za pomocą NumPy w sposób wektorowy.
        """
        array = surfarray.array3d(image).astype(np.float32)
        array = np.transpose(array, (1, 0, 2))  # [height][width][3]

        padded_array = np.pad(array, ((1, 1), (1, 1), (0, 0)), mode='edge')

        high_pass_kernel = np.array([[ 0, -1,  0],
                                     [-1,  5, -1],
                                     [ 0, -1,  0]], dtype=np.float32)

        filtered_array = np.empty_like(array)

        try:
            from numpy.lib.stride_tricks import sliding_window_view
        except ImportError:
            raise ImportError("Your NumPy version does not support sliding_window_view. Please update NumPy to >=1.20.")

        for c in range(3):
            channel = padded_array[:, :, c]  # [height+2, width+2]
            windows = sliding_window_view(channel, (3, 3))  # [height, width, 3, 3]

            convolution = np.sum(windows * high_pass_kernel, axis=(2, 3))

            convolution = np.clip(convolution, 0, 255)

            filtered_array[:, :, c] = convolution

        filtered_array = np.clip(filtered_array, 0, 255).astype(np.uint8)
        filtered_image = pygame.surfarray.make_surface(np.transpose(filtered_array, (1, 0, 2)))  # [width][height][3]
        return filtered_image

    def apply_gaussian_blur_numpy(self, image, kernel_size=5, sigma=1.0):
        array = surfarray.array3d(image).astype(np.float32)
        array = np.transpose(array, (1, 0, 2))

        ax = np.linspace(-(kernel_size // 2), kernel_size // 2, kernel_size)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-(xx**2 + yy**2) / (2. * sigma**2))
        kernel = kernel / np.sum(kernel)

        pad_size = kernel_size // 2
        padded_array = np.pad(array, ((pad_size, pad_size), (pad_size, pad_size), (0, 0)), mode='edge')

        filtered_array = np.empty_like(array)

        for c in range(3):
            channel = padded_array[:, :, c]
            # Wyciągnięcie okien o rozmiarze kernel_size x kernel_size
            windows = sliding_window_view(channel, (kernel_size, kernel_size))
            # Zastosowanie konwolucji
            filtered_channel = np.sum(windows * kernel, axis=(2, 3))
            # Przypisanie przefiltrowanych wartości do tablicy wynikowej
            filtered_array[:, :, c] = filtered_channel

        filtered_array = np.clip(filtered_array, 0, 255).astype(np.uint8)

        filtered_image = pygame.surfarray.make_surface(np.transpose(filtered_array, (1, 0, 2)))
        return filtered_image

    def apply_custom_convolution(self, image, kernel):
        array = surfarray.array3d(image).astype(np.float32)
        array = np.transpose(array, (1, 0, 2))  # [height][width][3]

        filtered_array = np.empty_like(array)

        for c in range(3):
            filtered_channel = convolve(array[:, :, c], kernel, mode='reflect')
            filtered_array[:, :, c] = filtered_channel

        filtered_array = np.clip(filtered_array, 0, 255).astype(np.uint8)
        filtered_image = pygame.surfarray.make_surface(np.transpose(filtered_array, (1, 0, 2)))
        return filtered_image
