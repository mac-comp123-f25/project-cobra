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
        self.obstacles = []
        for _ in range(count):
            while True:
                x = random.randint(0, (self.width // self.block_size) - 1) * self.block_size
                y = random.randint(0, (self.height // self.block_size) - 1) * self.block_size

                if [x, y] not in snake_body and [x, y] not in self.obstacles and [x, y] != food_pos:
                    self.obstacles.append([x, y])
                    break

    def draw(self, window):
        """Draw obstacles as GRAY squares"""
        GRAY = (100, 100, 100)
        for obs in self.obstacles:
            pygame.draw.rect(window, GRAY, (obs[0], obs[1], self.block_size, self.block_size))

    def check_collision(self, snake_head):
        """Returns True if snake hits any obstacle"""
        return snake_head in self.obstacles
