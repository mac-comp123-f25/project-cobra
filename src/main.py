from src.wa.member1 import Food, CollisionDetector, Score
from src.wa.member2 import *
from src.wa.member3 import *

"""
Main Snake Game - Brings everyone's work together
Uses: Game_Snake.py as base + member1.py (Elma's work)
"""
import pygame
import sys

# this initialize pygame
pygame.init()

# window size
WIDTH, HEIGHT = 600, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cobra Snake Game")

# all colors
GREEN = (108, 187, 60)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# snake (from Game_Snake.py)
snake_pos = [100, 50]
snake_body = [[100, 50], [80, 50], [60, 50]]  # Full snake body
snake_size = 20
snake_direction = 'RIGHT'
change_to = snake_direction

#game objects (this ia from member1.py)
food = Food(WIDTH, HEIGHT, snake_size)
collision = CollisionDetector(WIDTH, HEIGHT)
score = Score()

clock = pygame.time.Clock()

# game states
game_over = False
game_started = False


def draw_start_screen():
    """Draw simple start screen"""
    window.fill(BLACK)
    font_title = pygame.font.Font(None, 64)
    font_text = pygame.font.Font(None, 32)

    title = font_title.render('COBRA SNAKE', True, GREEN)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    window.blit(title, title_rect)

    start = font_text.render('Press SPACE to Start', True, WHITE)
    start_rect = start.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    window.blit(start, start_rect)


def draw_game_over():
    """Draw game over screen"""
    font_large = pygame.font.Font(None, 64)
    font_small = pygame.font.Font(None, 32)

    game_over_text = font_large.render('GAME OVER', True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    window.blit(game_over_text, game_over_rect)

    score_text = font_small.render(f'Final Score: {score.score}', True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    window.blit(score_text, score_rect)

    restart = font_small.render('Press SPACE to Restart', True, WHITE)
    restart_rect = restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    window.blit(restart, restart_rect)


def reset_game():
    """Reset everything"""
    global snake_pos, snake_body, snake_direction, change_to, game_over, game_started
    snake_pos = [100, 50]
    snake_body = [[100, 50], [80, 50], [60, 50]]
    snake_direction = 'RIGHT'
    change_to = snake_direction
    food.respawn(snake_body)
    score.reset()
    game_over = False
    game_started = False


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # start or restart
            if event.key == pygame.K_SPACE:
                if not game_started:
                    game_started = True
                elif game_over:
                    reset_game()
                    game_started = True

            # controls (and they prevent 180° turns)
            if game_started and not game_over:
                if event.key == pygame.K_UP and snake_direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                    change_to = 'RIGHT'

    #filling th background
    window.fill(GREEN)

    if not game_started:
        draw_start_screen()
    elif game_over:
        # Draw final state
        for segment in snake_body:
            pygame.draw.rect(window, BLUE, (segment[0], segment[1], snake_size, snake_size))
        food.draw(window)
        draw_game_over()
    else:
        # this update direction
        snake_direction = change_to

        #Move snake
        if snake_direction == 'UP':
            snake_pos[1] -= snake_size
        elif snake_direction == 'DOWN':
            snake_pos[1] += snake_size
        elif snake_direction == 'LEFT':
            snake_pos[0] -= snake_size
        elif snake_direction == 'RIGHT':
            snake_pos[0] += snake_size

        # added new head position
        snake_body.insert(0, list(snake_pos))

        # check if snake ate food (using collision detector)
        if collision.check_food_collision(snake_pos, food.position):
            score.add_points(10)  #score system
            food.respawn(snake_body)  # food respawn
        else:
            snake_body.pop()  # Remove tail if no food eaten

        #checking collisions (using collision detector)
        if collision.check_wall_collision(snake_pos):
            game_over = True

        if collision.check_self_collision(snake_body):
            game_over = True

        # Draw everything
        for segment in snake_body:
            pygame.draw.rect(window, BLUE, (segment[0], segment[1], snake_size, snake_size))

        food.draw(window)  # food drawing
        score.draw(window)  #score display

    pygame.display.update()
    clock.tick(10)