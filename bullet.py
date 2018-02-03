import pygame
from pygame.sprite import Sprite

# Using Sprites allows to group related elements in a game and act on all the grouped elements at once.


class Bullet(Sprite):
    """A class that manages bullets fired from ship"""

    def __init__(self, ai_settings, screen, ship):
        """Create a bullet object at the ship's current position"""

        super(Bullet, self).__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) and then set correct position.
        # Builds the bullet from the scratch. (0, 0) is for (x, y) coordinates
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store the bullet's position in decimal values
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the screen"""

        # Update the decimal position of the bullet
        self.y -= self.speed_factor

        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
