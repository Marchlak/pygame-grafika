import pygame
import numpy as np
from collections import deque
from scipy.ndimage import median_filter
from model.basic_binarisation_model import BasicBinarisationModel
from sklearn.cluster import KMeans


class AnalyzeModel:
    def __init__(self):
        """
        Initialize the AnalyzeModel without an image.
        """
        self.image_surface = None
        self.width = 0
        self.height = 0
        self.pixels = None
        self.green_threshold = 100
        self.green_pixels = None
        self.green_percentage = 0.0
        self.largest_green_area = 0
        self.largest_green_percentage = 0.0
        self.largest_region_coords = []
        self.binarized_image_surface = None
        self.binarization_method_used = ""
        self.binarization_model = BasicBinarisationModel()
        self.segmented_image_surface = None
        self.last_message = ""

    def set_image(self, image_surface):
        """
        Set the image surface and preprocess the pixel data.
        """
        self.image_surface = image_surface
        self.width, self.height = self.image_surface.get_size()
        self.pixels = pygame.surfarray.array3d(self.image_surface)
        self.last_message = f"Image set with size: {self.width}x{self.height}"

    def automatic_binarization(self):
        """
        Automatically detects the best binarization algorithm for the image and applies it.
        """
        if self.image_surface is None:
            self.last_message = "No image set for binarization."
            return

        image_array = pygame.surfarray.array3d(self.image_surface)
        grayscale_image = self._to_grayscale(image_array)

        global_mean = grayscale_image.mean()

        block_size = 32
        local_means = []
        for i in range(0, grayscale_image.shape[0], block_size):
            for j in range(0, grayscale_image.shape[1], block_size):
                block = grayscale_image[i : i + block_size, j : j + block_size]
                local_means.append(block.mean())

        local_means = np.array(local_means)
        mean_difference = np.abs(local_means - global_mean)
        mean_difference_std = mean_difference.std()

        print(f"Global mean: {global_mean}")
        print(f"Mean difference std: {mean_difference_std}")

        if mean_difference_std < 15:
            # Use global binarization
            self.last_message = "Using global binarization (Otsu's method)."
            self.binarized_image_surface = self.binarization_model.otsu_threshold(
                self.image_surface
            )
            self.binarization_method_used = "Otsu's method"
        else:
            self.last_message = "Using local binarization (Sauvola's method)."
            self.binarized_image_surface = self.binarization_model.sauvola_threshold(
                self.image_surface
            )
            self.binarization_method_used = "Sauvola's method"

    def _to_grayscale(self, image_array):
        """
        Convert an RGB image array to grayscale.
        """
        return (
            0.2989 * image_array[:, :, 0]
            + 0.5870 * image_array[:, :, 1]
            + 0.1140 * image_array[:, :, 2]
        ).astype(np.uint8)

    def get_binarization_results(self):
        """
        Return the binarized image and the method used.
        """
        return {
            "binarized_image": self.binarized_image_surface,
            "method_used": self.binarization_method_used,
        }

    def preprocess_image(self):
        """
        Automatically detect and remove noise and adjust histogram if needed.
        """
        if self.pixels is None:
            self.last_message = "No image set for preprocessing."
            return

        pixels_transposed = np.transpose(self.pixels, (1, 0, 2))

        gray_image = np.mean(pixels_transposed, axis=2).astype(np.uint8)

        num_zeros = np.sum(gray_image == 0)
        num_ones = np.sum(gray_image == 255)
        total_pixels = self.width * self.height
        noise_percentage = ((num_zeros + num_ones) / total_pixels) * 100

        self.last_message = f"Detected noise percentage: {noise_percentage:.2f}%"

        median_applied = False

        if noise_percentage > 0.5:
            self.last_message = (
                "Salt-and-pepper noise detected, applying median filter."
            )

            filtered_pixels_transposed = np.zeros_like(pixels_transposed)
            for c in range(3):
                filtered_pixels_transposed[:, :, c] = median_filter(
                    pixels_transposed[:, :, c], size=3
                )

            pixels_transposed = filtered_pixels_transposed
            median_applied = True
        else:
            self.last_message = "No significant noise detected."

        mean_intensity = np.mean(gray_image)
        self.last_message = f"Mean intensity: {mean_intensity}"

        histogram_adjusted = False

        if mean_intensity < 100 or mean_intensity > 155:
            self.last_message = "Adjusting histogram..."
            min_val = np.min(pixels_transposed)
            max_val = np.max(pixels_transposed)
            pixels_transposed = (
                (pixels_transposed - min_val) / (max_val - min_val) * 255
            ).astype(np.uint8)
            histogram_adjusted = True
        else:
            print("Histogram is within normal range, no adjustment needed.")

        if median_applied or histogram_adjusted:
            # Transpose back to (width, height, 3)
            self.pixels = np.transpose(pixels_transposed, (1, 0, 2))
            # Update the image surface
            self.image_surface = pygame.surfarray.make_surface(self.pixels)
            self.last_message = "Image preprocessing completed."
        else:
            print("No preprocessing was necessary.")

    def calculate_green_pixels(self, threshold=None):
        if self.pixels is None:
            self.last_message = "No image set for analysis."
            return

        if threshold is not None:
            self.green_threshold = threshold

        green_channel = self.pixels[:, :, 1]
        self.green_pixels = green_channel > self.green_threshold
        total_green = np.sum(self.green_pixels)
        total_pixels = self.width * self.height
        self.green_percentage = (total_green / total_pixels) * 100
        print(f"Total green pixels: {total_green}")
        print(f"Total pixels: {total_pixels}")
        print(f"Green percentage: {self.green_percentage:.2f}%")
        print(f"green_pixels shape: {self.green_pixels.shape}")  # Debug

    def find_largest_green_region(self):
        """
        Find the largest contiguous green region using BFS.
        """
        if self.green_pixels is None:
            print("Green pixels not calculated.")
            return

        visited = np.zeros((self.width, self.height), dtype=bool)
        largest_area = 0
        largest_region_coords = []

        for x in range(self.width):
            for y in range(self.height):
                if self.green_pixels[x, y] and not visited[x, y]:
                    region_coords = []
                    area = self.bfs(x, y, visited, region_coords)
                    if area > largest_area:
                        largest_area = area
                        largest_region_coords = region_coords

        self.largest_green_area = largest_area
        self.largest_green_percentage = (
            largest_area / (self.width * self.height)
        ) * 100
        self.largest_region_coords = largest_region_coords
        print(f"Largest green area: {self.largest_green_area} pixels")
        print(f"Largest green percentage: {self.largest_green_percentage:.2f}%")

    def bfs(self, start_x, start_y, visited, region_coords):
        """
        Perform Breadth-First Search to find all connected green pixels.
        """
        queue = deque()
        queue.append((start_x, start_y))
        visited[start_x, start_y] = True
        area = 1
        region_coords.append((start_x, start_y))

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            x, y = queue.popleft()
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width) and (0 <= ny < self.height):
                    if self.green_pixels[nx, ny] and not visited[nx, ny]:
                        queue.append((nx, ny))
                        visited[nx, ny] = True
                        area += 1
                        region_coords.append((nx, ny))

        return area

    def analyze_green(self):
        """
        Perform the full analysis on the image.
        """
        if self.image_surface is None:
            self.last_message = "No image set for analysis."
            return
        self.calculate_green_pixels()
        self.find_largest_green_region()

    def get_analysis_green_results(self):
        """
        Return the analysis results.
        """
        return {
            "green_percentage": self.green_percentage,
            "largest_green_area": self.largest_green_area,
            "largest_green_percentage": self.largest_green_percentage,
            "largest_region_coords": self.largest_region_coords,
        }

    def image_segmentation(self, n_clusters=5):
        """
        Perform image segmentation using K-Means clustering.
        """
        if self.image_surface is None:
            self.last_message = "No image set for segmentation."
            return

        image_array = pygame.surfarray.array3d(self.image_surface)
        pixels = image_array.reshape(-1, 3)

        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(pixels)
        labels = kmeans.labels_
        cluster_centers = kmeans.cluster_centers_.astype(np.uint8)

        segmented_pixels = cluster_centers[labels]
        segmented_image_array = segmented_pixels.reshape(image_array.shape)

        self.segmented_image_surface = pygame.surfarray.make_surface(
            segmented_image_array
        )
        self.last_message = "Image segmentation completed."

    def get_segmentation_result(self):
        """
        Return the segmented image.
        """
        return self.segmented_image_surface
