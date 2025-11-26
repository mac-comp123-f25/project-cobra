import pygame
import sys

# Initialize pygame
pygame.init()

# Window size
WIDTH, HEIGHT = 600, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game Starter")

# Colors
GREEN = (108, 187, 60)
BLUE = (0, 0, 255)

# Snake starting position + size
snake_pos = [100, 50]
snake_size = 20  # each block is 20x20

clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fill background green
    window.fill(GREEN)

    # Draw the snake (just one blue square for now)
    pygame.draw.rect(window, BLUE, (snake_pos[0], snake_pos[1], snake_size, snake_size))

    pygame.display.update()
    clock.tick(10)

()