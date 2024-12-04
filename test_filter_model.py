# test_filter_model.py

import unittest
import pygame
from model.filter_model import FilterModel
import numpy as np

class TestFilterModel(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.filter_model = FilterModel()
        self.image = pygame.Surface((3, 3), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        colors = [
            (0, 0, 0),       
            (255, 255, 255), 
            (0, 0, 0),       
            (255, 255, 255), 
            (0, 0, 0),       
            (255, 255, 255), 
            (0, 0, 0),       
            (255, 255, 255), 
            (0, 0, 0),      
        ]
        for y in range(3):
            for x in range(3):
                self.image.set_at((x, y), colors[y * 3 + x])

    def test_apply_smoothing_filter(self):
        filtered_image = self.filter_model.apply_smoothing_filter(self.image)
        original_array = np.transpose(pygame.surfarray.array3d(self.image), (1, 0, 2))
        filtered_array = np.transpose(pygame.surfarray.array3d(filtered_image), (1, 0, 2))
        
        expected_array = [
            [(113, 113, 113), (113, 113, 113), (113, 113, 113)],
            [(113, 113, 113), (113, 113, 113), (113, 113, 113)],
            [(113, 113, 113), (113, 113, 113), (113, 113, 113)],
        ]

        for y in range(3):  
            for x in range(3): 
                expected_r, expected_g, expected_b = expected_array[y][x]
                actual_r, actual_g, actual_b = filtered_array[y, x]
                self.assertAlmostEqual(actual_r, expected_r, delta=5,
                                       msg=f"R channel mismatch at ({x}, {y}): {actual_r} != {expected_r}")
                self.assertAlmostEqual(actual_g, expected_g, delta=5,
                                       msg=f"G channel mismatch at ({x}, {y}): {actual_g} != {expected_g}")
                self.assertAlmostEqual(actual_b, expected_b, delta=5,
                                       msg=f"B channel mismatch at ({x}, {y}): {actual_b} != {expected_b}")

    def test_apply_median_filter_numpy(self):
        filtered_image = self.filter_model.apply_median_filter_numpy(self.image)
        filtered_array = np.transpose(pygame.surfarray.array3d(filtered_image), (1, 0, 2))  
        
        expected_array = [
            [(0, 0, 0), (0, 0, 0), (0, 0, 0)],
            [(0, 0, 0), (0, 0, 0), (0, 0, 0)],
            [(0, 0, 0), (0, 0, 0), (0, 0, 0)],
        ]

        for y in range(3):
            for x in range(3): 
                expected_r, expected_g, expected_b = expected_array[y][x]
                actual_r, actual_g, actual_b = filtered_array[y, x]
                self.assertAlmostEqual(actual_r, expected_r, delta=2,
                                       msg=f"R channel mismatch at ({x}, {y}): {actual_r} != {expected_r}")
                self.assertAlmostEqual(actual_g, expected_g, delta=2,
                                       msg=f"G channel mismatch at ({x}, {y}): {actual_g} != {expected_g}")
                self.assertAlmostEqual(actual_b, expected_b, delta=2,
                                       msg=f"B channel mismatch at ({x}, {y}): {actual_b} != {expected_b}")

    def test_apply_sobel_filter_numpy(self):
        filtered_image = self.filter_model.apply_sobel_filter_numpy(self.image)
        filtered_array = np.transpose(pygame.surfarray.array3d(filtered_image), (1, 0, 2))  
        
        expected_array = [
            [(255, 255, 255), (0, 0, 0), (255, 255, 255)],
            [(0, 0, 0), (0, 0, 0), (0, 0, 0)],
            [(255, 255, 255), (0, 0, 0), (255, 255, 255)],
        ]

        for y in range(3):  # height
            for x in range(3):  # width
                expected_r, expected_g, expected_b = expected_array[y][x]
                actual_r, actual_g, actual_b = filtered_array[y, x]
                self.assertAlmostEqual(actual_r, expected_r, delta=50,
                                       msg=f"R channel mismatch at ({x}, {y}): {actual_r} != {expected_r}")
                self.assertAlmostEqual(actual_g, expected_g, delta=50,
                                       msg=f"G channel mismatch at ({x}, {y}): {actual_g} != {expected_g}")
                self.assertAlmostEqual(actual_b, expected_b, delta=50,
                                       msg=f"B channel mismatch at ({x}, {y}): {actual_b} != {expected_b}")

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()

