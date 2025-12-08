"""
member3.py - Initial Game Prototype (Phase 1)
Author: Kampe R & Elma M
Description: Early prototype with basic pygame setup and static snake
Note: This was our starting point. The complete game is in MainGame.py
"""
import pygame
import sys


def run_prototype():
    """
    Run the Phase 1 prototype - basic window with static blue square.
    This demonstrates our initial pygame setup before adding game mechanics.
    """
    # Initialize pygame
    pygame.init()

    # Window size
    WIDTH, HEIGHT = 600, 400
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game Starter - Phase 1")

    # Colors
    GREEN = (108, 187, 60)
    BLUE = (0, 0, 255)

    # Snake starting position + size
    snake_pos = [100, 50]
    snake_size = 20

    clock = pygame.time.Clock()

    # Basic game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill background green
        window.fill(GREEN)

        # Draw the snake (just one blue square - no movement yet)
        pygame.draw.rect(window, BLUE, (snake_pos[0], snake_pos[1], snake_size, snake_size))

        pygame.display.update()
        clock.tick(10)

    pygame.quit()

