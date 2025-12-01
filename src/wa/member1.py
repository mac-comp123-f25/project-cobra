"""
member1.py: work on Food and Collisions
Elma M
"""
import pygame
import random


# FOOD CLASS - makes the red squares appear randomly
class Food:
    def __init__(self, width, height, size=20):
        self.size = size
        self.width = width
        self.height = height
        # start with a random position
        self.position = self.generate_position()

    def generate_position(self):
        # need to make sure food appears on the grid, not randomly anywhere
        # so we use multiples of 20 (the snake size)
        x = random.randint(0, (self.width // self.size) - 1) * self.size
        y = random.randint(0, (self.height // self.size) - 1) * self.size
        return [x, y]

    def respawn(self, snake_body):
        # keep generating new positions until we find one that's not on the snake
        while True:
            self.position = self.generate_position()
            if self.position not in snake_body:
                break  # found a good spot!

    def draw(self, window):
        # just a red square
        RED = (255, 0, 0)
        pygame.draw.rect(window, RED,
                         (self.position[0], self.position[1], self.size, self.size))


# COLLISION DETECTOR - checks if snake hits stuff
class CollisionDetector:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

    def check_wall_collision(self, snake_head):
        # did the snake go off the screen?
        x, y = snake_head
        if x < 0 or x >= self.screen_width:
            return True
        if y < 0 or y >= self.screen_height:
            return True
        return False

    def check_food_collision(self, snake_head, food_position):
        # is the snake head on the same spot as food?
        return snake_head == food_position

    def check_self_collision(self, snake_body):
        # did the snake run into itself?
        head = snake_body[0]
        # check if head position is anywhere in the rest of the body
        return head in snake_body[1:]


# SCORE - keeps track of points
class Score:
    def __init__(self):
        self.score = 0

    def add_points(self, points=10):
        # add points when snake eats food
        self.score += points

    def reset(self):
        # start over
        self.score = 0

    def draw(self, window):
        # show score in top left corner
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        window.blit(score_text, (10, 10))