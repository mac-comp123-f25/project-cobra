"""
Main Cobra Snake Game
Team: Elma M, Kampe R, Providence T, Jack
Description: Classic Snake game with three difficulty levels, obstacles, and music
"""
from src.wa.member1 import Snake, Food, CollisionDetector, Score
from src.wa.member2 import draw_checkered_background
from src.wa.member4 import Obstacles

import pygame
import sys

# Initialize Pygame
pygame.init()

# Load and setup background music
pygame.mixer.music.load("assets/backgroundmusic.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
music_on = True

# Load music toggle icons
music_icon_on = pygame.image.load("assets/music_on.png")
music_icon_off = pygame.image.load("assets/music_off.png")
icon_size = 32
music_icon_on = pygame.transform.scale(music_icon_on, (icon_size, icon_size))
music_icon_off = pygame.transform.scale(music_icon_off, (icon_size, icon_size))
music_rect = pygame.Rect(10, 50, icon_size, icon_size)

# Load and scale start screen logo
cobra_logo = pygame.image.load("assets/StartGame_Cobra.png")
cobra_logo = pygame.transform.scale(cobra_logo, (600, 400))

# Window setup
WIDTH, HEIGHT = 600, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cobra Snake Game")

# Color definitions
GREEN = (108, 187, 60)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize game objects
snake = Snake(100, 60, 20)
food = Food(WIDTH, HEIGHT, 20)
collision = CollisionDetector(WIDTH, HEIGHT)
score = Score()
obstacles = Obstacles(WIDTH, HEIGHT, 20)

clock = pygame.time.Clock()

# Game state variables
game_over = False
game_started = False
difficulty = None
OBSTACLE_COUNT = 8


def draw_start_screen():
    """Display start screen with logo and difficulty selection menu."""
    # Dark background
    window.fill((20, 20, 20))

    # Center box
    box_width = 380
    box_height = 280
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2

    # Box background
    box_surface = pygame.Surface((box_width, box_height))
    box_surface.fill((40, 40, 40))
    window.blit(box_surface, (box_x, box_y))

    # Double border for depth
    pygame.draw.rect(window, (100, 200, 80), (box_x, box_y, box_width, box_height), 4)  # Green border
    pygame.draw.rect(window, (100, 100, 100), (box_x - 2, box_y - 2, box_width + 4, box_height + 4), 1)

    # Title with shadow
    font_title = pygame.font.Font(None, 60)
    shadow = font_title.render('COBRA SNAKE', True, (30, 60, 30))
    title = font_title.render('COBRA SNAKE', True, (100, 200, 80))

    title_rect = title.get_rect(center=(WIDTH // 2, box_y + 50))
    window.blit(shadow, (title_rect.x + 2, title_rect.y + 2))
    window.blit(title, title_rect)

    # Subtitle
    font_subtitle = pygame.font.Font(None, 22)
    subtitle = font_subtitle.render('Select Difficulty', True, (150, 150, 150))
    window.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, box_y + 95)))

    # Difficulty options with clean spacing
    font_option = pygame.font.Font(None, 32)

    y_start = box_y + 135
    spacing = 40

    # Easy
    easy = font_option.render('1  -  EASY', True, (100, 200, 80))
    window.blit(easy, easy.get_rect(center=(WIDTH // 2, y_start)))

    # Medium
    medium = font_option.render('2  -  MEDIUM', True, (255, 215, 0))
    window.blit(medium, medium.get_rect(center=(WIDTH // 2, y_start + spacing)))

    # Hard
    hard = font_option.render('3  -  HARD', True, (255, 100, 100))
    window.blit(hard, hard.get_rect(center=(WIDTH // 2, y_start + spacing * 2)))

    # Music icon in corner (outside box)
    if music_on:
        window.blit(music_icon_on, (15, 15))
    else:
        window.blit(music_icon_off, (15, 15))


def draw_game_over():
    """Display game over screen with final score and restart options."""
    # Dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(220)
    overlay.fill((20, 20, 20))
    window.blit(overlay, (0, 0))

    # Center box with rounded corners effect
    box_width = 350
    box_height = 200
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2

    # Box background
    box_surface = pygame.Surface((box_width, box_height))
    box_surface.fill((40, 40, 40))
    window.blit(box_surface, (box_x, box_y))

    # Double border for depth
    pygame.draw.rect(window, (255, 100, 100), (box_x, box_y, box_width, box_height), 4)
    pygame.draw.rect(window, (100, 100, 100), (box_x - 2, box_y - 2, box_width + 4, box_height + 4), 1)

    # Title with shadow
    font_title = pygame.font.Font(None, 56)
    shadow = font_title.render('GAME OVER', True, (80, 0, 0))
    title = font_title.render('GAME OVER', True, (255, 50, 50))

    title_rect = title.get_rect(center=(WIDTH // 2, box_y + 50))
    window.blit(shadow, (title_rect.x + 2, title_rect.y + 2))
    window.blit(title, title_rect)

    # Score with larger emphasis
    font_score = pygame.font.Font(None, 42)
    score_text = font_score.render(f'{score.score}', True, (255, 215, 0))  # Gold
    window.blit(score_text, score_text.get_rect(center=(WIDTH // 2, box_y + 105)))

    # Small label
    font_label = pygame.font.Font(None, 20)
    label = font_label.render('FINAL SCORE', True, (150, 150, 150))
    window.blit(label, label.get_rect(center=(WIDTH // 2, box_y + 85)))

    # Controls
    font_small = pygame.font.Font(None, 24)
    restart = font_small.render('SPACE to Restart', True, (200, 200, 200))
    menu = font_small.render('ESC for Menu', True, (150, 150, 150))
    window.blit(restart, restart.get_rect(center=(WIDTH // 2, box_y + 145)))
    window.blit(menu, menu.get_rect(center=(WIDTH // 2, box_y + 170)))


def restart_game():
    """Restart game at same difficulty level."""
    global game_over, game_started

    # Reset snake to starting position
    snake.body = [[100, 60], [80, 60], [60, 60]]
    snake.direction = 'RIGHT'
    snake.growing = False

    # Clear and regenerate obstacles
    obstacles.obstacles = []
    if difficulty in ['medium', 'hard']:
        obstacles.generate_obstacles(snake.body, food.position, OBSTACLE_COUNT)

    # Respawn food
    food.respawn(snake.body, obstacles.obstacles if difficulty in ['medium', 'hard'] else None)

    # Reset score
    score.reset()

    game_over = False
    game_started = True


def return_to_menu():
    """Return to start screen to select new difficulty."""
    global game_over, game_started, difficulty

    # Reset everything
    snake.body = [[100, 60], [80, 60], [60, 60]]
    snake.direction = 'RIGHT'
    snake.growing = False
    score.reset()

    # Clear difficulty and obstacles
    difficulty = None
    obstacles.obstacles = []

    game_over = False
    game_started = False


# ============================================================================
# MAIN GAME LOOP
# ============================================================================
if __name__ == "__main__":
    while True:
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Music toggle on click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if music_rect.collidepoint(event.pos):
                    if music_on:
                        pygame.mixer.music.pause()
                        music_on = False
                    else:
                        pygame.mixer.music.unpause()
                        music_on = True

            # Keyboard input
            if event.type == pygame.KEYDOWN:
                # Difficulty selection (before game starts)
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

                # Options after game over
                if game_over:
                    if event.key == pygame.K_SPACE:
                        restart_game()
                        continue
                    elif event.key == pygame.K_ESCAPE:
                        return_to_menu()
                        continue

                # Movement controls (during active gameplay)
                if game_started and not game_over:
                    if event.key == pygame.K_UP:
                        snake.direction = 'UP'
                    elif event.key == pygame.K_DOWN:
                        snake.direction = 'DOWN'
                    elif event.key == pygame.K_LEFT:
                        snake.direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT:
                        snake.direction = 'RIGHT'

        # RENDERING
        # Draw checkered background during gameplay (from member2)
        if game_started and not game_over:
            draw_checkered_background(window, WIDTH, HEIGHT)
        else:
            window.fill(GREEN)

        # Always draw music icon on top
        if music_on:
            window.blit(music_icon_on, (music_rect.x, music_rect.y))
        else:
            window.blit(music_icon_off, (music_rect.x, music_rect.y))

        # STATE-BASED RENDERING
        if not game_started and difficulty is None:
            # START SCREEN
            draw_start_screen()

        elif game_over:
            # GAME OVER SCREEN
            snake.draw(window)
            food.draw(window)
            if difficulty in ['medium', 'hard']:
                obstacles.draw(window)
            draw_game_over()

        else:
            # ACTIVE GAMEPLAY
            snake.move()

            # Check food collision
            if collision.check_food_collision(snake.body[0], food.position):
                snake.grow()
                score.add_points(10)
                food.respawn(snake.body, obstacles.obstacles if difficulty in ['medium', 'hard'] else None)

            # Check wall collision
            if collision.check_wall_collision(snake.body[0]):
                game_over = True

            # Check self collision
            if collision.check_self_collision(snake.body):
                game_over = True

            # Check obstacle collision (medium/hard only)
            if difficulty in ['medium', 'hard']:
                if obstacles.check_collision(snake.body[0]):
                    game_over = True

            # Draw all game objects
            snake.draw(window)
            food.draw(window)
            if difficulty in ['medium', 'hard']:
                obstacles.draw(window)
            score.draw(window)

        # FRAME RATE CONTROL (difficulty-based speed)
        if difficulty == 'easy':
            clock.tick(10)
        elif difficulty == 'medium':
            clock.tick(10)
        elif difficulty == 'hard':
            clock.tick(15)
        else:
            clock.tick(10)

        pygame.display.update()