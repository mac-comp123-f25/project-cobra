"""
member4.py - Difficulty System and Obstacles
Author: Jack
Description: Manages obstacle generation and collision detection for medium/hard modes
"""
import pygame
import random


class Obstacles:
    """
    Manages obstacle generation and collision for medium/hard difficulty levels.

    Attributes:
        width (int): Game window width
        height (int): Game window height
        block_size (int): Size of each obstacle block in pixels
        obstacles (list): List of [x, y] obstacle positions
    """

    def __init__(self, width, height, block_size=20):
        """
        Initialize obstacles system.

        Args:
            width (int): Game window width
            height (int): Game window height
            block_size (int): Size of obstacle blocks (default: 20)
        """
        self.width = width
        self.height = height
        self.block_size = block_size
        self.obstacles = []

    def generate_obstacles(self, snake_body, food_pos, count=5):
        """
        Generate random obstacles avoiding snake and food positions.
        Obstacles won't spawn within 3 blocks of the snake.

        Args:
            snake_body (list): List of snake segment positions to avoid
            food_pos (list): Food position to avoid
            count (int): Number of obstacles to generate (default: 5)
        """
        self.obstacles = []
        SAFE_DISTANCE = 3  # blocks away from snake

        for _ in range(count):
            while True:
                x = random.randint(0, (self.width // self.block_size) - 1) * self.block_size
                y = random.randint(0, (self.height // self.block_size) - 1) * self.block_size

                position = [x, y]

                # Don't spawn on snake or food or other obstacles
                if position in snake_body or position in self.obstacles or position == food_pos:
                    continue

                # Check safe distance from all snake segments
                too_close = False
                for segment in snake_body:
                    distance_x = abs(x - segment[0]) // self.block_size
                    distance_y = abs(y - segment[1]) // self.block_size

                    if distance_x <= SAFE_DISTANCE and distance_y <= SAFE_DISTANCE:
                        too_close = True
                        break

                # If not too close, add obstacle
                if not too_close:
                    self.obstacles.append(position)
                    break

    def draw(self, window):
        """
        Draw all obstacles as gray squares.

        Args:
            window (pygame.Surface): Game window surface to draw on
        """
        GRAY = (100, 100, 100)
        for obs in self.obstacles:
            pygame.draw.rect(window, GRAY, (obs[0], obs[1], self.block_size, self.block_size))

    def check_collision(self, snake_head):
        """
        Check if snake head collided with any obstacle.

        Args:
            snake_head (list): [x, y] coordinates of snake head

        Returns:
            bool: True if collision detected, False otherwise
        """
        return snake_head in self.obstacles