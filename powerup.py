import pygame
import random
from config import *


class PowerUp:
    """Reto 11: special object that falls from the top and players can pick up.

    Kinds:
      - "speed":  temporary speed boost
      - "life":   recovers one life (never above LIVES_PER_PLAYER)
      - "shield": temporary invulnerability
    """

    def __init__(self):
        self.kind = random.choice(list(POWERUP_TYPES))
        self.color, self.letter = POWERUP_TYPES[self.kind]
        x = random.randint(0, WIDTH - POWERUP_SIZE)
        self.rect = pygame.Rect(x, -POWERUP_SIZE, POWERUP_SIZE, POWERUP_SIZE)
        self.speed = POWERUP_FALL_SPEED

    def move(self):
        """Move the power-up down the screen"""
        self.rect.y += self.speed

    def is_off_screen(self):
        return self.rect.y > HEIGHT

    def apply(self, player, now):
        """Apply the effect to the player that picked it up. `now` is the game time in ms"""
        if self.kind == "speed":
            player.boost_until = now + POWERUP_EFFECT_TIME
        elif self.kind == "shield":
            player.shield_until = now + POWERUP_EFFECT_TIME
        elif self.kind == "life":
            player.lives = min(LIVES_PER_PLAYER, player.lives + 1)

    def draw(self, surface, font):
        """Draw a colored circle with a letter inside"""
        pygame.draw.circle(surface, self.color, self.rect.center, POWERUP_SIZE // 2)
        text = font.render(self.letter, True, (0, 0, 0))
        surface.blit(text, text.get_rect(center=self.rect.center))
