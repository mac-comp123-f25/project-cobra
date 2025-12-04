"""
member2.py: work on Background
Thusa
"""
import pygame

# window size
WIDTH, HEIGHT = 600, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cobra Snake Game")

# softer green shades for the checkered background
LIGHT_GREEN = (130, 200, 100)
DARK_GREEN = (110, 180, 80)

TILE_SIZE = 40  # size of each checkered square

def draw_checkered_background():
    for row in range(HEIGHT // TILE_SIZE + 1):
        for col in range(WIDTH // TILE_SIZE + 1):
            # alternate colors like a chessboard
            if (row + col) % 2 == 0:
                color = LIGHT_GREEN
            else:
                color = DARK_GREEN
            pygame.draw.rect(
                window,
                color,
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )
draw_checkered_background()

# ON GAME SCREEN
if game_started and not game_over:
    draw_checkered_background()

# keep window open
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
