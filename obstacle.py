import pygame
import random
from config import *  # Import all constants from the config module


class Obstacle:
    """An obstacle that the player must avoid"""

    def __init__(self):
        # Reto 2: random size between 20 and 70 px
        size = random.randint(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE)
        # The size is chosen BEFORE x, so the obstacle always fits inside the window width
        x = random.randint(0, WIDTH - size)
        self.rect = pygame.Rect(x, -size, size, size)
        self.color = random.choice(OBSTACLE_COLORS)  # Random color for the obstacle
        self.speed = random.randint(2, 7)  # Random speed for the obstacle

    def move(self):
        """Move the obstacle down the screen"""
        self.rect.y += self.speed

    def is_off_screen(self):
        """Check if the obstacle has moved off the screen"""
        return self.rect.y > HEIGHT

    def draw(self, surface):
        """Draw the obstacle on the given surface"""
        pygame.draw.rect(surface, self.color, self.rect)
