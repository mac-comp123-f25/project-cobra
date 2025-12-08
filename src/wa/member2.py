"""
member2.py - Background and Visual Enhancements
Author: Thusa
Description: Checkered background pattern for gameplay
"""
import pygame

# Color definitions for checkered background
LIGHT_GREEN = (130, 200, 100)
DARK_GREEN = (110, 180, 80)

# Tile size for checkered pattern
TILE_SIZE = 40


def draw_checkered_background(window, width, height):
    """
    Draw alternating light and dark green checkered pattern.

    Args:
        window (pygame.Surface): Game window surface to draw on
        width (int): Width of the game window
        height (int): Height of the game window
    """
    for row in range(height // TILE_SIZE + 1):
        for col in range(width // TILE_SIZE + 1):
            # Alternate colors like a chessboard
            if (row + col) % 2 == 0:
                color = LIGHT_GREEN
            else:
                color = DARK_GREEN
            pygame.draw.rect(
                window,
                color,
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )