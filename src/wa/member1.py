"""
member1.py: Core game classes for Snake, Food, Collision Detection, and Score
Author: Elma M
Description: Contains the main game mechanics for Cobra Snake game
"""
import pygame
import random


class Snake:
    """
    Represents the snake player in the game.

    Attributes:
        size (int): Size of each snake segment in pixels
        body (list): List of [x, y] coordinates for each snake segment
        direction (str): Current movement direction ('UP', 'DOWN', 'LEFT', 'RIGHT')
        growing (bool): Flag indicating if snake should grow on next move
    """

    def __init__(self, x, y, size=20):
        """
        Initialize the snake at given position.

        Args:
            x (int): Starting x-coordinate
            y (int): Starting y-coordinate
            size (int): Size of each snake segment (default: 20)
        """
        self.size = size
        self.body = [[x, y], [x - size, y], [x - 2 * size, y]]
        self.direction = 'RIGHT'
        self.growing = False

    def move(self):
        """
        Move the snake one step in the current direction.
        Adds new head segment and removes tail unless growing.
        """
        head = self.body[0]
        if self.direction == 'UP':
            new = [head[0], head[1] - self.size]
        elif self.direction == 'DOWN':
            new = [head[0], head[1] + self.size]
        elif self.direction == 'LEFT':
            new = [head[0] - self.size, head[1]]
        else:  # RIGHT
            new = [head[0] + self.size, head[1]]

        self.body.insert(0, new)  # add new head

        if not self.growing:
            self.body.pop()  # remove tail
        else:
            self.growing = False  # reset flag after growing

    def grow(self):
        """Set flag to grow snake by one segment on next move."""
        self.growing = True

    def draw(self, window):
        """
        Draw the snake on the game window with animated eyes.

        Args:
            window (pygame.Surface): Game window surface to draw on
        """
        BLUE = (0, 0, 255)
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        for i, seg in enumerate(self.body):
            pygame.draw.rect(window, BLUE, (seg[0], seg[1], self.size, self.size))

            # Draw eyes only on the head
            if i == 0:
                cx = seg[0] + self.size // 2
                cy = seg[1] + self.size // 2
                eye_radius = self.size // 4
                pupil_radius = self.size // 8

                # Eye placement changes based on movement direction
                if self.direction == "UP":
                    eye1 = (cx - 6, cy - 7)
                    eye2 = (cx + 6, cy - 7)
                    pupil_offset = (0, -2)
                elif self.direction == "DOWN":
                    eye1 = (cx - 6, cy + 7)
                    eye2 = (cx + 6, cy + 7)
                    pupil_offset = (0, +2)
                elif self.direction == "LEFT":
                    eye1 = (cx - 7, cy - 6)
                    eye2 = (cx - 7, cy + 6)
                    pupil_offset = (-2, 0)
                else:  # RIGHT
                    eye1 = (cx + 7, cy - 6)
                    eye2 = (cx + 7, cy + 6)
                    pupil_offset = (+2, 0)

                # Draw eyeballs
                pygame.draw.circle(window, WHITE, eye1, eye_radius)
                pygame.draw.circle(window, WHITE, eye2, eye_radius)

                # Draw pupils
                pygame.draw.circle(window, BLACK,
                                 (eye1[0] + pupil_offset[0], eye1[1] + pupil_offset[1]),
                                 pupil_radius)
                pygame.draw.circle(window, BLACK,
                                 (eye2[0] + pupil_offset[0], eye2[1] + pupil_offset[1]),
                                 pupil_radius)


class Food:
    """
    Represents food items that the snake can eat.

    Attributes:
        size (int): Size of food item in pixels
        width (int): Game window width
        height (int): Game window height
        position (list): Current [x, y] position of food
    """

    def __init__(self, width, height, size=20):
        """
        Initialize food at a random grid position.

        Args:
            width (int): Game window width
            height (int): Game window height
            size (int): Size of food item (default: 20)
        """
        self.size = size
        self.width = width
        self.height = height
        self.position = self.generate_position()

    def generate_position(self):
        """
        Generate random grid-aligned position for food.

        Returns:
            list: [x, y] coordinates aligned to grid
        """
        x = random.randint(0, (self.width // self.size) - 1) * self.size
        y = random.randint(0, (self.height // self.size) - 1) * self.size
        return [x, y]

    def respawn(self, snake_body, obstacles=None):
        """
        Move food to new position, avoiding snake body and obstacles.

        Args:
            snake_body (list): List of snake segment positions
            obstacles (list, optional): List of obstacle positions to avoid
        """
        while True:
            self.position = self.generate_position()
            if self.position not in snake_body:
                if obstacles is None or self.position not in obstacles:
                    break

    def draw(self, window):
        """
        Draw food as an apple with stem and leaf.

        Args:
            window (pygame.Surface): Game window surface to draw on
        """
        RED = (255, 0, 0)
        BROWN = (139, 69, 19)
        GREEN = (0, 255, 0)

        # Draw apple body (circle)
        center_x = self.position[0] + self.size // 2
        center_y = self.position[1] + self.size // 2
        radius = self.size // 2
        pygame.draw.circle(window, RED, (center_x, center_y), radius)

        # Draw stem
        pygame.draw.rect(window, BROWN,
                        (center_x - 2, center_y - radius - 3, 4, 6))

        # Draw leaf
        pygame.draw.ellipse(window, GREEN,
                           (center_x + 2, center_y - radius, 8, 5))


class CollisionDetector:
    """
    Handles collision detection for game boundaries, food, and self-collision.

    Attributes:
        screen_width (int): Width of game window
        screen_height (int): Height of game window
    """

    def __init__(self, screen_width, screen_height):
        """
        Initialize collision detector with screen dimensions.

        Args:
            screen_width (int): Width of game window
            screen_height (int): Height of game window
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

    def check_wall_collision(self, snake_head):
        """
        Check if snake head has hit any wall.

        Args:
            snake_head (list): [x, y] coordinates of snake head

        Returns:
            bool: True if collision detected, False otherwise
        """
        x, y = snake_head
        if x < 0 or x >= self.screen_width:
            return True
        if y < 0 or y >= self.screen_height:
            return True
        return False

    def check_food_collision(self, snake_head, food_position):
        """
        Check if snake head is on same position as food.

        Args:
            snake_head (list): [x, y] coordinates of snake head
            food_position (list): [x, y] coordinates of food

        Returns:
            bool: True if positions match, False otherwise
        """
        return snake_head[0] == food_position[0] and snake_head[1] == food_position[1]

    def check_self_collision(self, snake_body):
        """
        Check if snake head has collided with its own body.

        Args:
            snake_body (list): List of all snake segment positions

        Returns:
            bool: True if head is in body, False otherwise
        """
        head = snake_body[0]
        return head in snake_body[1:]


class Score:
    """
    Manages and displays the player's score.

    Attributes:
        score (int): Current score value
    """

    def __init__(self):
        """Initialize score at zero."""
        self.score = 0

    def add_points(self, points=10):
        """
        Add points to current score.

        Args:
            points (int): Number of points to add (default: 10)
        """
        self.score += points

    def reset(self):
        """Reset score to zero."""
        self.score = 0

    def draw(self, window):
        """
        Display current score on game window.

        Args:
            window (pygame.Surface): Game window surface to draw on
        """
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        window.blit(score_text, (10, 10))