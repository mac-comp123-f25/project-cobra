from src.wa.member1 import Snake, Food, CollisionDetector, Score
from src.wa.member2 import *
from src.wa.member3 import *
from src.wa.member4 import *

"""
Main Snake Game - Updated with Difficulty Levels
Uses: Game_Snake.py as base + member1.py (Elma's work) + member2 (level system)
"""

import pygame
import sys

pygame.init()
pygame.mixer.music.load("backgroundmusic.mp3")   # load your music file
pygame.mixer.music.set_volume(0.5)          # set volume (0.0 - 1.0)
pygame.mixer.music.play(-1)                 # -1 = loop indefinitely
music_on = True                              # track if music is on



music_icon_on = pygame.image.load("music_on.png")
music_icon_off = pygame.image.load("music_off.png")
icon_size = 32
music_icon_on = pygame.transform.scale(music_icon_on, (icon_size, icon_size))
music_icon_off = pygame.transform.scale(music_icon_off, (icon_size, icon_size))
music_rect = pygame.Rect(10, 50, icon_size, icon_size)  # top-left corner

cobra_logo = pygame.image.load("StartGame_Cobra.png")
cobra_logo = pygame.transform.scale(cobra_logo, (600, 400))  # adjust size



# window size
WIDTH, HEIGHT = 600, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cobra Snake Game")

# colors
GREEN = (108, 187, 60)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# snake object
snake = Snake(100, 60, 20)

# game objects
food = Food(WIDTH, HEIGHT, 20)
collision = CollisionDetector(WIDTH, HEIGHT)
score = Score()

clock = pygame.time.Clock()

# game states
game_over = False
game_started = False

# difficulty system
difficulty = None              # "easy", "medium", "hard"
obstacles = Obstacles(WIDTH, HEIGHT, 20)
OBSTACLE_COUNT = 8             # number of obstacles for medium/hard


def draw_start_screen():
    """Start screen with difficulty options"""
    window.fill(BLACK)
    window.blit(cobra_logo, (0, 0))

    # draw music icon
    if music_on:
        window.blit(music_icon_on, (music_rect.x, music_rect.y))
    else:
        window.blit(music_icon_off, (music_rect.x, music_rect.y))

    # difficulty options
    font_small = pygame.font.Font(None, 20)  # Smaller font (was 24)
    corner_x = 15  # Left side
    corner_y = 90  # Below music icon
    box_surface = pygame.Surface((110, 90))  # Smaller box
    box_surface.set_alpha(180)
    box_surface.fill(BLACK)
    window.blit(box_surface, (corner_x - 5, corner_y - 5))

    #difficulty options
    title_text = font_small.render('SELECT:', True, WHITE)
    window.blit(title_text, (corner_x, corner_y))

    easy = font_small.render('1 - Easy', True, GREEN)
    window.blit(easy, (corner_x, corner_y + 20))

    medium = font_small.render('2 - Medium', True, (255, 255, 0))
    window.blit(medium, (corner_x, corner_y + 40))

    hard = font_small.render('3 - Hard', True, (255, 100, 100))
    window.blit(hard, (corner_x, corner_y + 60))


def draw_game_over():
    """Game over UI"""
    font_large = pygame.font.Font(None, 64)
    font_small = pygame.font.Font(None, 32)

    game_over_text = font_large.render('GAME OVER', True, (255, 0, 0))
    window.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3)))

    score_text = font_small.render(f'Final Score: {score.score}', True, WHITE)
    window.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    restart = font_small.render('Press SPACE to Restart', True, WHITE)
    window.blit(restart, restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))


def reset_game():
    """Reset everything"""
    global game_over, game_started, difficulty

    snake.body = [[100, 60], [80, 60], [60, 60]]
    snake.direction = 'RIGHT'
    snake.growing = False

    food.respawn(snake.body, obstacles.obstacles if difficulty in ['medium','hard'] else None)

    score.reset()

    # reset difficulty
    difficulty = None
    obstacles.obstacles = []

    game_over = False
    game_started = False



# MAIN GAME LOOP
while True:


    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            #  MUSIC TOGGLE

        if event.type == pygame.MOUSEBUTTONDOWN:
            if music_rect.collidepoint(event.pos):
                if music_on:
                    pygame.mixer.music.pause()
                    music_on = False
                else:
                    pygame.mixer.music.unpause()
                    music_on = True

        if event.type == pygame.KEYDOWN:

            # difficulty selection BEFORE game starts
            if not game_started and difficulty is None:
                if event.key == pygame.K_1:
                    difficulty = 'easy'
                    game_started = True

                elif event.key == pygame.K_2:
                    difficulty = 'medium'
                    obstacles.generate_obstacles(snake.body, food.position, OBSTACLE_COUNT)
                    game_started = True

                elif event.key == pygame.K_3:
                    difficulty = 'hard'
                    obstacles.generate_obstacles(snake.body, food.position, OBSTACLE_COUNT)
                    game_started = True

            # restart after game over
            if event.key == pygame.K_SPACE and game_over:
                reset_game()
                continue

            # movement controls when game is active
            if game_started and not game_over:
                if event.key == pygame.K_UP:
                    snake.direction = 'UP'
                elif event.key == pygame.K_DOWN:
                    snake.direction = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    snake.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    snake.direction = 'RIGHT'

    window.fill(GREEN)

    if music_on:
        window.blit(music_icon_on, (music_rect.x, music_rect.y))
    else:
        window.blit(music_icon_off, (music_rect.x, music_rect.y))


    # ON START SCREEN
    if not game_started and difficulty is None:
        draw_start_screen()


    # ON GAME OVER
    elif game_over:
        snake.draw(window)
        food.draw(window)
        if difficulty in ['medium', 'hard']:
            obstacles.draw(window)
        draw_game_over()


    # ACTIVE GAMEPLAY
    else:
        snake.move()

        # food collision
        if collision.check_food_collision(snake.body[0], food.position):
            snake.grow()
            score.add_points(10)
            food.respawn(snake.body, obstacles.obstacles if difficulty in ['medium','hard'] else None)


        # wall collision
        if collision.check_wall_collision(snake.body[0]):
            game_over = True

        # self collision
        if collision.check_self_collision(snake.body):
            game_over = True

        # obstacle collision (medium/hard only)
        if difficulty in ['medium', 'hard']:
            if obstacles.check_collision(snake.body[0]):
                game_over = True

        # drawing
        snake.draw(window)
        food.draw(window)

        if difficulty in ['medium', 'hard']:
            obstacles.draw(window)

        score.draw(window)


    # SPEED CONTROL
    if difficulty == 'easy':
        clock.tick(10)
    elif difficulty == 'medium':
        clock.tick(10)
    elif difficulty == 'hard':
        clock.tick(18)
    pygame.display.update()
