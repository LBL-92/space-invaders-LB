import pygame
from config import *
from player import Player
from obstacle import Obstacle
from powerup import PowerUp
from scores import save_score, top_scores

# Game states
STATE_MENU = "menu"            # start screen with the top 5 (reto 12)
STATE_PLAYING = "playing"
STATE_NAME_INPUT = "name"      # game over: asking the player's name (reto 12)
STATE_GAME_OVER = "game_over"  # waiting for R to restart (reto 5)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Player Game")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 26)
big_font = pygame.font.Font(None, 80)

# Create the player objects
player = Player(*PLAYER1_START)
player2 = Player(*PLAYER2_START, PLAYER_COLOR2, PLAYER2_SPEED)
players = [player, player2]

high_score = 0  # Reto 9: best score of this execution (NOT reset on restart)
state = STATE_MENU
paused = False
player_name = ""
best_scores = top_scores()  # Reto 12: the five best scores read from scores.txt

# These variables are (re)initialized in reset_game()
obstacles = []
powerups = []
score = 0
game_time = 0          # ms of real play (does not advance during pause or game over)
last_obstacle_spawn_time = 0
last_powerup_spawn_time = 0


def reset_game():
    """Reto 5: start a new game. The high score is kept."""
    global obstacles, powerups, score, game_time
    global last_obstacle_spawn_time, last_powerup_spawn_time, paused, player_name
    for p in players:
        p.reset()  # initial position, lives, speed and effects
    obstacles = []
    powerups = []
    score = 0
    game_time = 0
    last_obstacle_spawn_time = 0
    last_powerup_spawn_time = 0
    paused = False
    player_name = ""


def get_spawn_delay():
    """Reto 7: every 10 points the delay drops 50 ms, never below 150 ms"""
    level = score // POINTS_PER_LEVEL
    return max(MIN_SPAWN_DELAY, SPAWN_OBSTACLE_DELAY - SPAWN_DELAY_STEP * level)


def draw_centered(text, text_font, color, y):
    surf = text_font.render(text, True, color)
    screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))


def draw_overlay():
    """Dark translucent layer so the messages are easy to read"""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))


def draw_top_scores(y):
    draw_centered(f"TOP {TOP_SCORES_SHOWN}", font, (255, 255, 0), y)
    if not best_scores:
        draw_centered("No scores yet", small_font, (200, 200, 200), y + 40)
    for i, (name, value) in enumerate(best_scores):
        draw_centered(f"{i + 1}. {name} - {value}", small_font, (255, 255, 255), y + 40 + i * 28)


def draw_hud():
    """Score, record, survival time and lives"""
    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
    screen.blit(font.render(f"Best: {high_score}", True, (255, 215, 0)), (10, 40))
    time_text = font.render(f"Time: {game_time // 1000} s", True, (255, 255, 255))
    screen.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))
    # Lives and speed of each player
    for i, p in enumerate(players):
        text = small_font.render(f"P{i + 1} lives: {p.lives}  speed: {p.speed}", True, p.color)
        screen.blit(text, (WIDTH - text.get_width() - 10, 45 + i * 24))


# GAME LOOP
running = True
while running:
    dt = clock.tick(FPS)  # milliseconds since the previous frame

    # ------------------------------------------------------------------ events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if state == STATE_MENU:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    reset_game()
                    state = STATE_PLAYING

            elif state == STATE_PLAYING:
                if event.key == pygame.K_ESCAPE:  # Reto 4: pause / resume
                    paused = not paused
                elif not paused:
                    # Reto 8: one KEYDOWN = one change (holding the key does nothing)
                    if event.key in (pygame.K_PLUS, pygame.K_KP_PLUS) or event.unicode == "+":
                        player.change_speed(1)
                    elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS) or event.unicode == "-":
                        player.change_speed(-1)

            elif state == STATE_NAME_INPUT:
                # Reto 12: text input implemented with Pygame events
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    save_score(player_name, score)
                    best_scores = top_scores()
                    state = STATE_GAME_OVER
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.unicode.isprintable() and event.unicode != "" and len(player_name) < MAX_NAME_LENGTH:
                    player_name += event.unicode

            elif state == STATE_GAME_OVER:
                if event.key == pygame.K_r:  # Reto 5: restart
                    reset_game()
                    state = STATE_PLAYING

    # ------------------------------------------------------------------ update
    if state == STATE_PLAYING and not paused:
        # Reto 6 / 4: game_time only advances while playing, so it is the
        # clock for the survival timer, spawns, invulnerability and power-ups
        game_time += dt

        # OBSTACLES spawning logic (reto 7: delay depends on the score)
        if game_time - last_obstacle_spawn_time > get_spawn_delay():
            obstacles.append(Obstacle())
            last_obstacle_spawn_time = game_time

        # POWER-UPS spawning logic (reto 11)
        if game_time - last_powerup_spawn_time > POWERUP_SPAWN_DELAY:
            powerups.append(PowerUp())
            last_powerup_spawn_time = game_time

        # Update the player's position (dead players don't move)
        for p in players:
            p.update_effects(game_time)
        if player.is_alive():
            player.moveArrows()
        if player2.is_alive():
            player2.moveWASD()

        # Update the position of each obstacle and check collisions (retos 3 and 10)
        remaining_obstacles = []
        for obstacle in obstacles:
            obstacle.move()
            hit = False
            for p in players:
                if p.is_alive() and p.rect.colliderect(obstacle.rect):
                    if p.hit(game_time):
                        hit = True  # the obstacle is destroyed by the impact
            if hit:
                continue
            if obstacle.is_off_screen():
                score += 1  # Increment the score for each obstacle that goes off screen
            else:
                remaining_obstacles.append(obstacle)
        obstacles = remaining_obstacles

        # Power-ups: move, pick up and remove (reto 11)
        remaining_powerups = []
        for powerup in powerups:
            powerup.move()
            picked = False
            for p in players:
                if p.is_alive() and p.rect.colliderect(powerup.rect):
                    powerup.apply(p, game_time)
                    picked = True
                    break
            if not picked and not powerup.is_off_screen():
                remaining_powerups.append(powerup)
        powerups = remaining_powerups

        # Reto 9: update the record
        if score > high_score:
            high_score = score

        # Game over when BOTH players have no lives left (retos 3 and 10)
        if not player.is_alive() and not player2.is_alive():
            state = STATE_NAME_INPUT

    # -------------------------------------------------------------------- draw
    screen.fill(BACKGROUND_COLOR)
    for p in players:
        p.draw(screen, game_time)
    for obstacle in obstacles:
        obstacle.draw(screen)  # Draw each obstacle
    for powerup in powerups:
        powerup.draw(screen, small_font)

    if state != STATE_MENU:
        draw_hud()

    if state == STATE_MENU:
        draw_overlay()
        draw_centered("OBSTACLE DODGER", big_font, (255, 255, 255), 90)
        draw_top_scores(220)
        draw_centered("Press ENTER to start", font, (0, 255, 0), 460)
        draw_centered("P1: arrows (+/- speed)   P2: WASD   ESC: pause", small_font, (200, 200, 200), 510)

    elif state == STATE_PLAYING and paused:
        draw_overlay()
        draw_centered("PAUSE", big_font, (255, 255, 255), HEIGHT // 2 - 40)

    elif state == STATE_NAME_INPUT:
        draw_overlay()
        draw_centered("Game Over", big_font, (255, 0, 0), 120)
        draw_centered(f"Score: {score}   Time: {game_time // 1000} s", font, (255, 255, 255), 220)
        draw_centered("Enter your name and press ENTER:", font, (255, 255, 255), 300)
        cursor = "_" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
        draw_centered(player_name + cursor, big_font, (0, 255, 255), 340)

    elif state == STATE_GAME_OVER:
        draw_overlay()
        draw_centered("Game Over", big_font, (255, 0, 0), 60)
        draw_centered(f"Score: {score}   Best: {high_score}", font, (255, 255, 255), 150)
        draw_top_scores(210)
        draw_centered("Press R to restart", font, (0, 255, 0), 460)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
