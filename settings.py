# Settings file contains the settings class. She initializes attributes controlling the game's appearance and
# the ship's sped.
from pygame.rect import Rect


class Settings:
    """A class that store all setting for Alien Invasion"""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings:
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (180, 208, 247)

        # Ship speed settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3  # in pixels
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # Fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings when leveling up"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

    def safe_rect(self):
        offset = 50
        return Rect(0 + offset, 0 + offset, self.screen_width - (offset * 2), self.screen_height - offset)

    def inside_horizontal(self, rect):
        safe = self.safe_rect()
        return rect.left >= safe.left and rect.right <= safe.right

    def inside_vertical(self, rect):
        safe = self.safe_rect()
        return rect.top >= safe.top and rect.bottom <= safe.bottom;

    def in_safe_rect(self, rect):
        return self.inside_horizontal(rect) and self.inside_vertical(rect)