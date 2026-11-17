import pygame
from config import *  # Import all constants from the config module

# Rectangle covering the whole window, used to keep the players inside it
SCREEN_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)


class Player:
    """The player controlled by the user"""

    def __init__(self, x, y, color=PLAYER_COLOR, speed=PLAYER_SPEED):
        """Initialize the player with a position and size"""
        self.start_pos = (x, y)
        self.color = color
        self.default_speed = speed
        self.rect = pygame.Rect(x, y, 50, 50)
        self.reset()

    def reset(self):
        """Put the player back in its initial state (used when restarting)"""
        self.rect.topleft = self.start_pos
        self.base_speed = self.default_speed   # speed chosen by the user (reto 8)
        self.speed = self.base_speed           # real speed (base + power-up boost)
        self.lives = LIVES_PER_PLAYER          # reto 10
        self.invulnerable_until = 0            # game time (ms) until which it can't be hit
        self.boost_until = 0                   # power-up: speed boost
        self.shield_until = 0                  # power-up: invulnerability

    # ------------------------------------------------------------------ movement
    def moveArrows(self):
        """Update the player's position based on keyboard input"""
        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        self.keep_inside_screen()

    def moveWASD(self):
        """Update the player's position based on WASD keyboard input"""
        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

        self.keep_inside_screen()

    def keep_inside_screen(self):
        """Reto 1: the player can't leave the window through any side"""
        self.rect.clamp_ip(SCREEN_RECT)

    # --------------------------------------------------------------------- speed
    def change_speed(self, amount):
        """Reto 8: change the base speed, always between MIN and MAX"""
        self.base_speed = max(MIN_PLAYER_SPEED, min(MAX_PLAYER_SPEED, self.base_speed + amount))

    # ------------------------------------------------------- lives / power-ups
    def is_alive(self):
        return self.lives > 0

    def is_invulnerable(self, now):
        return now < self.invulnerable_until or now < self.shield_until

    def hit(self, now):
        """Reto 10: lose one life unless invulnerable. Returns True if the hit counted"""
        if not self.is_alive() or self.is_invulnerable(now):
            return False
        self.lives -= 1
        self.invulnerable_until = now + INVULNERABILITY_TIME
        return True

    def update_effects(self, now):
        """Reto 11: temporary effects expire automatically"""
        if now < self.boost_until:
            self.speed = self.base_speed + SPEED_BOOST
        else:
            self.speed = self.base_speed

    # ---------------------------------------------------------------------- draw
    def draw(self, surface, now=0):
        """Draw the player on the given surface"""
        if not self.is_alive():
            return
        # Blink while invulnerable after a hit (every 100 ms)
        blinking = now < self.invulnerable_until and (now // 100) % 2 == 0
        if not blinking:
            pygame.draw.rect(surface, self.color, self.rect)
        # White border while the shield power-up is active
        if now < self.shield_until:
            pygame.draw.rect(surface, (255, 255, 255), self.rect.inflate(8, 8), 3)
