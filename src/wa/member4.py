import pygame
import random


# OBSTACLE by Jack

class Obstacles:
    def __init__(self, width, height, block_size=20):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.obstacles = []   # list of [x, y] obstacle positions

    def generate_obstacles(self, snake_body, food_pos, count=5):
        """
        Generate random obstacles avoiding snake and food positions.
        Obstacles won't spawn within 3 blocks of the snake.
        """
        self.obstacles = []
        SAFE_DISTANCE = 3  # blocks away from snake

        for _ in range(count):
            while True:
                x = random.randint(0, (self.width // self.block_size) - 1) * self.block_size
                y = random.randint(0, (self.height // self.block_size) - 1) * self.block_size

                # Check if position is valid
                position = [x, y]

                # Don't spawn on snake or food or other obstacles
                if position in snake_body or position in self.obstacles or position == food_pos:
                    continue

                # Check safe distance from all snake segments
                too_close = False
                for segment in snake_body:
                    distance_x = abs(x - segment[0]) // self.block_size
                    distance_y = abs(y - segment[1]) // self.block_size

                    # If within safe distance, mark as too close
                    if distance_x <= SAFE_DISTANCE and distance_y <= SAFE_DISTANCE:
                        too_close = True
                        break

                # If not too close, add obstacle
                if not too_close:
                    self.obstacles.append(position)
                    break

    def draw(self, window):
        """Draw obstacles as GRAY squares"""
        GRAY = (100, 100, 100)
        for obs in self.obstacles:
            pygame.draw.rect(window, GRAY, (obs[0], obs[1], self.block_size, self.block_size))

    def check_collision(self, snake_head):
        """Returns True if snake hits any obstacle"""
        return snake_head in self.obstacles
