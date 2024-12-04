# test_filter_model.py

import unittest
import pygame
from model.filter_model import FilterModel

class TestFilterModel(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.filter_model = FilterModel()
        # Tworzymy przykładowy obraz 3x3 z różnymi kolorami
        self.image = pygame.Surface((3, 3), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        colors = [
            (10, 20, 30),
            (40, 50, 60),
            (70, 80, 90),
            (100, 110, 120),
            (130, 140, 150),
            (160, 170, 180),
            (190, 200, 210),
            (220, 230, 240),
            (250, 255, 255),
        ]
        for y in range(3):
            for x in range(3):
                self.image.set_at((x, y), colors[y * 3 + x])

    def test_apply_smoothing_filter(self):
        filtered_image = self.filter_model.apply_smoothing_filter(self.image)
        original_array = pygame.surfarray.array3d(self.image)
        filtered_array = pygame.surfarray.array3d(filtered_image)
        
        expected_array = [
            [(10+20+40+50)/4, (20+30+50+60)/4, (30+60)/2],
            [(40+50+100+110)/4, (50+60+110+120)/4, (60+120)/2],
            [(100+110+190+200)/4, (110+120+200+210)/4, (120+210)/2],
        ]

        for y in range(3):
            for x in range(3):
                self.assertAlmostEqual(filtered_array[y, x, 0], expected_array[y][x], delta=1)
                self.assertAlmostEqual(filtered_array[y, x, 1], expected_array[y][x], delta=1)
                self.assertAlmostEqual(filtered_array[y, x, 2], expected_array[y][x], delta=1)

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()

