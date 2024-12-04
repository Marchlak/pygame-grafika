import numpy as np
import pygame
from PIL import Image

def create_low_contrast_image(width, height, base_value=125, noise_level=10):
    arr = np.full((height, width, 3), base_value, dtype=np.uint8)
    noise = np.random.randint(-noise_level, noise_level + 1, (height, width, 3), dtype=np.int16)
    arr = np.clip(arr.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    print(f"Low Contrast Image - shape: {arr.shape}, dtype: {arr.dtype}")
    return pygame.surfarray.make_surface(arr.transpose(1, 0, 2))  # Pygame expects (width, height, 3)

def create_gradient_image(width, height):
    gradient = np.tile(np.linspace(0, 255, width, dtype=np.uint8), (height, 1))
    arr = np.stack((gradient, gradient, gradient), axis=2)
    print(f"Gradient Image - shape: {arr.shape}, dtype: {arr.dtype}")
    return pygame.surfarray.make_surface(arr.transpose(1, 0, 2))

def create_limited_color_image(width, height, color_channel='G', min_val=100, max_val=150):
    arr = np.zeros((height, width, 3), dtype=np.uint8)
    if color_channel == 'R':
        arr[:, :, 0] = np.random.randint(min_val, max_val + 1, (height, width), dtype=np.uint8)
    elif color_channel == 'G':
        arr[:, :, 1] = np.random.randint(min_val, max_val + 1, (height, width), dtype=np.uint8)
    elif color_channel == 'B':
        arr[:, :, 2] = np.random.randint(min_val, max_val + 1, (height, width), dtype=np.uint8)
    else:
        raise ValueError("color_channel must be one of 'R', 'G', 'B'")
    print(f"Limited Color Image ({color_channel}) - shape: {arr.shape}, dtype: {arr.dtype}")
    return pygame.surfarray.make_surface(arr.transpose(1, 0, 2))

def create_block_image(width, height, block_size=128):
    arr = np.zeros((height, width, 3), dtype=np.uint8)
    num_blocks_x = width // block_size
    num_blocks_y = height // block_size
    colors = [
        [50, 100, 150],   # Blok 1
        [200, 150, 100],  # Blok 2
        [100, 150, 200],  # Blok 3
        [150, 200, 100],  # Blok 4
    ]
    
    for i in range(num_blocks_x):
        for j in range(num_blocks_y):
            color = colors[(i + j) % len(colors)]
            start_x = i * block_size
            start_y = j * block_size
            end_x = start_x + block_size
            end_y = start_y + block_size
            arr[start_y:end_y, start_x:end_x] = color
    
    print(f"Block Image - shape: {arr.shape}, dtype: {arr.dtype}")
    return pygame.surfarray.make_surface(arr.transpose(1, 0, 2))

def save_surface_as_png(surface, filename):
    """
    Zapisuje Pygame Surface jako plik PNG.
    """
    arr = pygame.surfarray.array3d(surface).transpose(1, 0, 2)  # Transpozycja na (height, width, 3)
    img = Image.fromarray(arr)
    img.save(filename)
    print(f"Image saved as {filename}")

def main():
    width, height = 512, 512  # Rozmiar obrazów

    # Inicjalizacja Pygame
    pygame.init()

    # Tworzenie obrazów
    low_contrast_surface = create_low_contrast_image(width, height)
    gradient_surface = create_gradient_image(width, height)
    limited_green_surface = create_limited_color_image(width, height, color_channel='G', min_val=100, max_val=150)
    block_surface = create_block_image(width, height, block_size=128)

    # Zapisywanie obrazów jako PNG
    save_surface_as_png(low_contrast_surface, "low_contrast_pygame.png")
    save_surface_as_png(gradient_surface, "gradient_pygame.png")
    save_surface_as_png(limited_green_surface, "limited_color_green_pygame.png")
    save_surface_as_png(block_surface, "blocks_pygame.png")

    # Zakończenie Pygame
    pygame.quit()

if __name__ == "__main__":
    main()

