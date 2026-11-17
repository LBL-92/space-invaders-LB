# Game constants
WIDTH = 800
HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)  # Black background
PLAYER_COLOR = (60, 140, 255)  # Blue player
PLAYER_COLOR2 = (255, 140, 60)  # Orange player
PLAYER_SPEED = 6  # Speed of the player movement
PLAYER2_SPEED = 2  # Speed of the second player (as in the original code)
OBSTACLE_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]  # Red, Green, Blue, Yellow, Magenta

# Starting positions (x, y)
PLAYER1_START = (375, 530)
PLAYER2_START = (100, 100)

# Reto 2: obstacle size range (pixels)
OBSTACLE_MIN_SIZE = 20
OBSTACLE_MAX_SIZE = 70

# Reto 7: increasing difficulty
SPAWN_OBSTACLE_DELAY = 500   # milliseconds (initial delay)
MIN_SPAWN_DELAY = 150        # the delay can never go below this
SPAWN_DELAY_STEP = 50        # reduction every POINTS_PER_LEVEL points
POINTS_PER_LEVEL = 10

# Reto 8: player 1 speed limits
MIN_PLAYER_SPEED = 2
MAX_PLAYER_SPEED = 12

# Reto 10: lives
LIVES_PER_PLAYER = 3
INVULNERABILITY_TIME = 2000  # milliseconds after being hit

# Reto 11: power-ups
POWERUP_SPAWN_DELAY = 8000   # milliseconds between power-ups
POWERUP_SIZE = 30
POWERUP_FALL_SPEED = 3
POWERUP_EFFECT_TIME = 5000   # milliseconds (speed boost / shield)
SPEED_BOOST = 4              # extra speed while the boost is active
# kind -> (color, letter shown inside)
POWERUP_TYPES = {
    "speed": ((0, 255, 255), "S"),
    "life": ((255, 80, 160), "+"),
    "shield": ((255, 255, 255), "I"),
}

# Reto 12: high scores file
SCORES_FILE = "scores.txt"
MAX_NAME_LENGTH = 12
TOP_SCORES_SHOWN = 5
